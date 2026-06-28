import flet as ft
import time

def main(page: ft.Page):
    # 1. Page Setup
    page.title = "SYS SENDER PRO"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.padding = 0

    # 2. Loading Page Component
    loading_screen = ft.Container(
        content=ft.Column(
            [
                ft.ProgressRing(color=ft.colors.BLUE_700, stroke_width=6),
                ft.Text("Starting System...", size=22, weight="bold", color=ft.colors.BLUE_900),
                ft.Text("Please wait a moment", size=14, color=ft.colors.GREY_700)
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        alignment=ft.alignment.center,
        expand=True,
        bgcolor=ft.colors.WHITE
    )

    # Force the UI to render the loading screen immediately
    page.add(loading_screen)
    page.update()

    try:
        # Simulate loading time for resources (3 seconds)
        time.sleep(3)

        # 3. Main Dashboard UI
        dashboard = ft.Container(
            content=ft.Column(
                [
                    ft.Icon(ft.icons.CHECK_CIRCLE, size=80, color=ft.colors.GREEN_600),
                    ft.Text("SYS SENDER", size=28, weight="bold"),
                    ft.Text("App is perfectly running!", size=16, color=ft.colors.GREEN_700),
                    ft.Divider(height=30, color=ft.colors.TRANSPARENT),
                    ft.ElevatedButton("Start Sending", icon=ft.icons.SEND, width=220, height=50),
                    ft.ElevatedButton("Settings", icon=ft.icons.SETTINGS, width=220, height=50),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            alignment=ft.alignment.center,
            expand=True,
        )

        # Remove loading screen and show Dashboard
        page.controls.clear()
        page.add(dashboard)
        page.update()

    except Exception as e:
        # If anything fails, it will show the error on screen instead of a black screen
        page.controls.clear()
        page.add(
            ft.Text(f"CRITICAL ERROR:\n{e}", color=ft.colors.RED, size=16, weight="bold")
        )
        page.update()

if __name__ == "__main__":
    ft.app(target=main)
