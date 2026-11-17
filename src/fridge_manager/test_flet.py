import flet as ft

def main(page: ft.Page) -> None:
    page.title = "Smart Fridge"
    page.add(ft.Text("Okienko Flet działa!"))

ft.run(main)