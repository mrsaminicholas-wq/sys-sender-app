import flet as ft
import base64
import json
import time
import os
from email.message import EmailMessage
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

def main(page: ft.Page):
    # --- System Page Setup ---
    page.title = "SYS_SENDER_V8 [MOBILE_TTY]"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#050505"
    page.padding = 12
    page.scroll = ft.ScrollMode.ADAPTIVE
    page.theme = ft.Theme(font_family="monospace")

    # Header Title
    header = ft.Text("root@sys-sender:~# ./execute_mobile --v 8.0", color="#00ff41", size=15, weight="bold")
    
    # --- Input Fields ---
    proxy_input = ft.TextField(
        label="[ VPN / PROXY ADDRESS ] (e.g. 103.111.43.12:8080)", 
        border_color="#008f11", color="#00ff41", text_size=12, height=45
    )

    token_input = ft.TextField(
        label="[ PASTE TOKEN.JSON CONTENT HERE ]", 
        multiline=True, min_lines=3, max_lines=3,
        border_color="#008f11", color="#00ff41", text_size=11
    )

    targets_input = ft.TextField(
        label="TARGET_EMAILS.TXT (One Per Line)", 
        multiline=True, min_lines=4, max_lines=6,
        border_color="#008f11", color="#00ff41", text_size=12
    )

    aliases_input = ft.TextField(
        label="ALIASES.TXT (Names - Optional)", 
        multiline=True, min_lines=2, max_lines=3,
        border_color="#008f11", color="#00ff41", text_size=12
    )

    subjects_input = ft.TextField(
        label="SUBJECTS.TXT (One Per Line)", 
        multiline=True, min_lines=2, max_lines=3,
        border_color="#008f11", color="#00ff41", text_size=12
    )

    payload_input = ft.TextField(
        label="PAYLOAD_BODY.HTML (Raw Code)", 
        multiline=True, min_lines=4, max_lines=6,
        border_color="#008f11", color="#00ff41", text_size=12
    )

    delay_slider = ft.Slider(min=1, max=15, divisions=14, label="{value} SEC", value=3, active_color="#00ff41")

    # --- Live Output Console ---
    console_output = ft.ListView(expand=True, spacing=2, auto_scroll=True, height=180)
    console_box = ft.Container(
        content=console_output,
        border=ft.border.all(1, "#00ff41"),
        padding=8, bgcolor="#000000", border_radius=3
    )

    def print_log(msg, color="#00ff41"):
        console_output.controls.append(ft.Text(f">> {msg}", color=color, size=11, font_family="monospace"))
        page.update()

    # --- Core Shooting Engine ---
    def execute_campaign(e):
        console_output.controls.clear()
        print_log("SYSTEM STARTING...", "#00bfff")

        # 1. Proxy Check
        p_val = proxy_input.value.strip() if proxy_input.value else ""
        if p_val:
            os.environ["HTTP_PROXY"] = f"http://{p_val}"
            os.environ["HTTPS_PROXY"] = f"http://{p_val}"
            print_log(f"[VPN] PROXY TUNNEL ROUTED: {p_val}", "#f59e0b")

        # 2. Token Check
        raw_token = token_input.value.strip() if token_input.value else ""
        if not raw_token:
            print_log("[ERR] TOKEN.JSON CANNOT BE EMPTY!", "#ff003c")
            return

        try:
            token_dict = json.loads(raw_token)
            SCOPES = ['https://www.googleapis.com/auth/gmail.send']
            creds = Credentials.from_authorized_user_info(token_dict, SCOPES)
            service = build('gmail', 'v1', credentials=creds)
            print_log("[AUTH] OAUTH2 TOKEN ACCEPTED.", "#00ff41")
        except Exception as ex:
            print_log(f"[ERR] TOKEN PARSE FAILED: {str(ex)[:35]}", "#ff003c")
            return

        # 3. Data Extraction
        targets = [t.strip() for t in targets_input.value.split('\n') if t.strip()] if targets_input.value else []
        aliases = [a.strip() for a in aliases_input.value.split('\n') if a.strip()] if aliases_input.value else [""]
        subjects = [s.strip() for s in subjects_input.value.split('\n') if s.strip()] if subjects_input.value else []
        html_code = payload_input.value.strip() if payload_input.value else ""

        if not targets or not subjects or not html_code:
            print_log("[ERR] TARGETS, SUBJECTS OR HTML IS NULL!", "#ff003c")
            return

        print_log(f"[SYS] TARGETS ACQUIRED: {len(targets)}", "#00bfff")

        # 4. Loop
        for idx, email in enumerate(targets):
            c_sub = subjects[idx % len(subjects)]
            c_alias = aliases[idx % len(aliases)] if aliases[0] else ""

            try:
                msg = EmailMessage()
                msg.set_content("HTML Payload Required.")
                msg.add_alternative(html_code, subtype='html')
                
                formatted_to = f"{c_alias} <{email}>" if c_alias else email
                msg['To'] = formatted_to
                msg['Subject'] = c_sub

                encoded_msg = base64.urlsafe_b64encode(msg.as_bytes()).decode()
                service.users().messages().send(userId="me", body={'raw': encoded_msg}).execute()

                print_log(f"[+] SENT -> {email}", "#00ff41")
            except Exception as s_err:
                print_log(f"[-] FAILED -> {email} | ERR: {str(s_err)[:20]}...", "#ff003c")

            if idx < len(targets) - 1:
                time.sleep(int(delay_slider.value))

        print_log("[SYS] CAMPAIGN FINISHED. EXIT CODE 0.", "#00bfff")

    # Send Button
    send_btn = ft.ElevatedButton(
        text="INITIATE_ATTACK_VECTOR", 
        color="#000000", bgcolor="#00ff41",
        on_click=execute_campaign, width=400, height=45
    )

    # UI Tree
    page.add(
        header,
        ft.Divider(color="#003b00", height=10),
        ft.Text("[ NETWORK & AUTH ]", color="#008f11", size=11, weight="bold"),
        proxy_input,
        token_input,
        ft.Divider(color="#003b00", height=10),
        ft.Text("[ TARGET PAYLOAD ]", color="#008f11", size=11, weight="bold"),
        targets_input,
        aliases_input,
        subjects_input,
        payload_input,
        ft.Text("ANTI-BAN THROTTLE DELAY (SEC)", color="#008f11", size=10),
        delay_slider,
        send_btn,
        ft.Divider(color="#003b00", height=10),
        ft.Text("[ STDOUT_LIVE_CONSOLE ]", color="#008f11", size=11, weight="bold"),
        console_box
    )

ft.app(target=main)
