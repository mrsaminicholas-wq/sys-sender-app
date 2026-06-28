import flet as ft
import asyncio

class AppDashboard(ft.UserControl):
    """
    This is the main dashboard component. 
    Using a Class structure makes the app scalable.
    """
    def build(self):
        return ft.Container(
            content=ft.Column(
                [
                    ft.Icon(ft.icons.DASHBOARD_ROUNDED, size=60, color=ft.colors.BLUE_700),
                    ft.Text("Dashboard", size=30, weight="bold"),
                    ft.Text("Welcome to your advanced SYS-SENDER application.", size=16),
                    ft.ElevatedButton("Process Data", icon=ft.icons.PLAY_ARROW, on_click=lambda _: print("Processing...")),
                    ft.ElevatedButton("View Logs", icon=ft.icons.LIST_ALT, on_click=lambda _: print("Viewing Logs...")),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=20,
            alignment=ft.alignment.center,
        )

async def main(page: ft.Page):
    page.title = "SYS SENDER PRO"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # --- Splash Screen Logic ---
    splash_screen = ft.Container(
        content=ft.Column(
            [
                ft.ProgressRing(color=ft.colors.BLUE_700, stroke_width=6),
                ft.Text("Initializing Application...", size=18, weight="bold"),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        alignment=ft.alignment.center,
        expand=True,
    )

    page.add(splash_screen)
    await page.update_async()

    # Simulate loading time
    await asyncio.sleep(2)

    # --- Switch to Dashboard ---
    page.controls.clear()
    page.add(AppDashboard())
    await page.update_async()

# Run the application
if __name__ == "__main__":
    ft.app(target=main)
ft.MainAxisAlignment.CENTER
