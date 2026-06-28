import flet as ft

def main(page: ft.Page):
    page.title = "Test App"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    
    # A simple text to confirm the app actually runs
    page.add(
        ft.Text("App is perfectly working!", size=25, weight="bold", color=ft.colors.GREEN)
    )

if __name__ == "__main__":
    ft.app(target=main)
