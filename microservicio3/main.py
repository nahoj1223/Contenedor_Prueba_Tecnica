import os
import flet as ft
from domain.entities.pricing import Pricing
from domain.entities.product import Product
from usecases.create_product_usecase import CreateProductUseCase
from usecases.get_product_usecase import GetProductUseCase
from usecases.list_products_usecase import ListProductsUseCase
from usecases.delete_product_usecase import DeleteProductUseCase
from usecases.check_final_price_usecase import CheckFinalPriceUseCase
from infrastructure.repositories.product_repository_api import ProductRepositoryAPI
from infrastructure.repositories.pricing_repository_api import PricingRepositoryAPI

def main(page: ft.Page):
    page.title = "Gestión de Productos"
    page.scroll = "auto"
    page.bgcolor = "#f0f2f5"
    page.horizontal_alignment = "center"

    # Dropdown para elegir acción (centrado y letra negra)
    action_dropdown = ft.Dropdown(
        label="Acción",
        width=350,
        options=[
            ft.dropdown.Option("Crear Producto"),
            ft.dropdown.Option("Obtener Producto"),
            ft.dropdown.Option("Listar Productos"),
            ft.dropdown.Option("Eliminar Producto"),
            ft.dropdown.Option("Consultar Precio Final")
        ],
        label_style=ft.TextStyle(color=ft.Colors.BLACK),
        text_style=ft.TextStyle(color=ft.Colors.BLACK)
    )

    # Campos para crear producto
    sku = ft.TextField(label="SKU", value="prueba-sku", width=350, label_style=ft.TextStyle(color=ft.Colors.BLACK), text_style=ft.TextStyle(color=ft.Colors.BLACK))
    name = ft.TextField(label="Nombre", value="lapicero", width=350, label_style=ft.TextStyle(color=ft.Colors.BLACK), text_style=ft.TextStyle(color=ft.Colors.BLACK))
    base_price = ft.TextField(label="Precio Base", value="5000", width=350, label_style=ft.TextStyle(color=ft.Colors.BLACK), text_style=ft.TextStyle(color=ft.Colors.BLACK))
    currency = ft.Dropdown(label="Moneda",width=350,
        options=[
            ft.dropdown.Option("COP"),
            ft.dropdown.Option("USD")
        ],
        value="COP",
        label_style=ft.TextStyle(color=ft.Colors.BLACK),
        text_style=ft.TextStyle(color=ft.Colors.BLACK)
    )
    category = ft.TextField(label="Categoría", value="utiles", width=350, label_style=ft.TextStyle(color=ft.Colors.BLACK), text_style=ft.TextStyle(color=ft.Colors.BLACK))
    
    #campos para obtener precio final
    country = ft.TextField(label="Pais", value="CO", width=350, label_style=ft.TextStyle(color=ft.Colors.BLACK), text_style=ft.TextStyle(color=ft.Colors.BLACK))
    coupon = ft.TextField(label="Cupon", value="BLACKFRIDAY", width=350, label_style=ft.TextStyle(color=ft.Colors.BLACK), text_style=ft.TextStyle(color=ft.Colors.BLACK))

    # Campo para obtener producto
    get_sku = ft.TextField(label="SKU a consultar", width=350, label_style=ft.TextStyle(color=ft.Colors.BLACK), text_style=ft.TextStyle(color=ft.Colors.BLACK))

    # Campo para borrar
    delete_sku = ft.TextField(label="SKU a eliminar", width=350, label_style=ft.TextStyle(color=ft.Colors.BLACK), text_style=ft.TextStyle(color=ft.Colors.BLACK))

    # Resultado de acciones
    result_text = ft.Text("", size=14, color=ft.Colors.BLACK)
    result_text_dict = ft.Text("", size=14, color=ft.Colors.BLACK)

    #Tarjeta para mostrar resultados
    result_card = ft.Card(
        content=ft.Container(
            content=result_text,
            padding=15,
            bgcolor=ft.Colors.GREY_100,
            border_radius=10,
        ),
        visible=False, 
        width=400,
    )

    #Tarjeta para mostrar resultados de diccionarios
    result_card_dict = ft.Card(
        content=ft.Container(
            content=result_text_dict,
            padding=15,
            bgcolor=ft.Colors.GREY_100,
            border_radius=10,
        ),
        visible=False, 
        width=400,
    )

    # Repositorios y casos de uso
    repositoryProduct = ProductRepositoryAPI(os.getenv("API_URL_PRODUCTS"))
    repositoryPricing = PricingRepositoryAPI(os.getenv("API_URL_PRICING"))

    create_use_case = CreateProductUseCase(repositoryProduct)
    get_use_case = GetProductUseCase(repositoryProduct)
    delete_use_case = DeleteProductUseCase(repositoryProduct)
    list_use_case = ListProductsUseCase(repositoryProduct)
    check_pricing_use_case = CheckFinalPriceUseCase(repositoryPricing)

    # Acciones
    def show_result(message: str, color=ft.Colors.BLACK):
        result_text.value = message
        result_text.color = color
        result_card_dict.visible = False
        result_card.visible = True
        page.update()
    
    def show_result_dict(data: dict, title: str):
        spans = [
            ft.TextSpan(title + "\n\n", style=ft.TextStyle(weight="bold", color=ft.Colors.BLUE_700))
        ]

        for key, value in data.items():
            spans.append(
                ft.TextSpan(
                    f"- {key}: ",
                    style=ft.TextStyle(weight="bold", color=ft.Colors.BLACK)  # Etiqueta en negrilla
                )
            )
            spans.append(
                ft.TextSpan(
                    f"{value}\n",
                    style=ft.TextStyle(color=ft.Colors.BLACK)  # Valor normal
                )
            )

        result_text_dict.spans = spans
        result_card.visible = False
        result_card_dict.visible = True
        page.update()

    def crear_producto(e):
        try:
            product = Product(
                sku=sku.value,
                name=name.value,
                base_price=float(base_price.value),
                currency=currency.value,
                category=category.value
            )
            created = create_use_case.execute(product)
            show_result(f"✅ Producto creado", color=ft.Colors.GREEN_700)
        except Exception as ex:
            show_result(f"❌ Error: {ex}", color=ft.Colors.GREEN_700)

    def obtener_producto(e):
        try:
            getted = get_use_case.execute(get_sku.value)

            if getted is None:
                show_result("❌ Producto no encontrado", color=ft.Colors.GREEN_700)
            else:
                show_result_dict(getted.__dict__, "✅ Producto obtenido")
        except Exception as ex:
            show_result(f"❌ Error: {ex}", color=ft.Colors.RED_700)
    
    def listar_productos(e):
        try:
            list_p = list_use_case.execute()

            if list_p is None:
                raise Exception("No hay productos disponibles")
            else:
                # Crear filas de la tabla
                rows = []
                for p in list_p["products"]:
                    rows.append(
                        ft.DataRow(cells=[
                            ft.DataCell(ft.Text(p.get("sku", ""))),
                            ft.DataCell(ft.Text(p.get("name", ""))),
                            ft.DataCell(ft.Text(str(p.get("base_price", "")))),
                            ft.DataCell(ft.Text(p.get("currency", ""))),
                            ft.DataCell(ft.Text(p.get("category", ""))),
                        ])
                    )

                # Crear la tabla
                data_table = ft.DataTable(
                    columns=[
                        ft.DataColumn(ft.Text("SKU", style=ft.TextStyle(weight="bold", color=ft.Colors.BLACK))),
                        ft.DataColumn(ft.Text("Nombre", style=ft.TextStyle(weight="bold", color=ft.Colors.BLACK))),
                        ft.DataColumn(ft.Text("Precio Base", style=ft.TextStyle(weight="bold", color=ft.Colors.BLACK))),
                        ft.DataColumn(ft.Text("Moneda", style=ft.TextStyle(weight="bold", color=ft.Colors.BLACK))),
                        ft.DataColumn(ft.Text("Categoría", style=ft.TextStyle(weight="bold", color=ft.Colors.BLACK))),
                    ],
                    rows=[
                        ft.DataRow(cells=[
                            ft.DataCell(ft.Text(p.get("sku", ""), color=ft.Colors.BLACK)),
                            ft.DataCell(ft.Text(p.get("name", ""), color=ft.Colors.BLACK)),
                            ft.DataCell(ft.Text(str(p.get("base_price", "")), color=ft.Colors.BLACK)),
                            ft.DataCell(ft.Text(p.get("currency", ""), color=ft.Colors.BLACK)),
                            ft.DataCell(ft.Text(p.get("category", ""), color=ft.Colors.BLACK)),
                        ])
                        for p in list_p["products"]
                    ],
                    border=ft.border.all(1, ft.Colors.GREY_300),
                    heading_row_color=ft.Colors.GREY_200,
                    heading_row_height=40,
                    data_row_min_height=30,
                    width=950,
                )

                # Mostrar tabla en el contenedor dinámico
                dynamic_content.controls.clear()
                dynamic_content.controls.append(data_table)
                result_card.visible = False  # Ocultar mensaje anterior
                page.update()

        except Exception as ex:
            show_result(f"❌ Error: {ex}", color=ft.Colors.RED_700)

    def borrar_producto(e):
        try:
            deleted = delete_use_case.execute(delete_sku.value)
            if deleted:
                show_result(f"🗑️ Producto {delete_sku.value} eliminado correctamente", color=ft.Colors.GREEN_700)
        except Exception as ex:
            show_result(f"❌ Error: {ex}", color=ft.Colors.RED_700)

    def consultar_precio_final(e):
        try:
            pricing = Pricing(
                sku=sku.value,
                country=country.value,
                coupon=coupon.value
            )
            check = check_pricing_use_case.execute(pricing)

            show_result_dict(check,"✅ Consulta Exitosa")
        except Exception as ex:
            show_result(f"❌ Error: {ex}", color=ft.Colors.GREEN_700)

    # Botones
    btn_create = ft.Row(
        [
            ft.ElevatedButton(
                "Crear Producto",
                on_click=crear_producto,
                style=ft.ButtonStyle(
                    bgcolor={ft.ControlState.DEFAULT: ft.Colors.BLUE_600},
                    color={ft.ControlState.DEFAULT: ft.Colors.WHITE},
                    shape=ft.RoundedRectangleBorder(radius=8),
                    padding=15
                )
            )
        ],
        alignment="center"
    )

    btn_get = ft.Row(
        [
            ft.ElevatedButton(
                "Obtener Producto",
                on_click=obtener_producto,
                style=ft.ButtonStyle(
                    bgcolor={ft.ControlState.DEFAULT: ft.Colors.BLUE_600},
                    color={ft.ControlState.DEFAULT: ft.Colors.WHITE},
                    shape=ft.RoundedRectangleBorder(radius=8),
                    padding=15
                )
            )
        ],
        alignment="center"
    )

    btn_list = ft.Row(
        [
            ft.ElevatedButton(
                "Listar",
                on_click=listar_productos,
                style=ft.ButtonStyle(
                    bgcolor={ft.ControlState.DEFAULT: ft.Colors.BLUE_600},
                    color={ft.ControlState.DEFAULT: ft.Colors.WHITE},
                    shape=ft.RoundedRectangleBorder(radius=8),
                    padding=15
                )
            )
        ],
        alignment="center"
    )

    btn_delete = ft.Row(
        [
            ft.ElevatedButton(
                "Eliminar Producto",
                on_click=borrar_producto,
                style=ft.ButtonStyle(
                    bgcolor={ft.ControlState.DEFAULT: ft.Colors.RED_600},
                    color={ft.ControlState.DEFAULT: ft.Colors.WHITE},
                    shape=ft.RoundedRectangleBorder(radius=8),
                    padding=15
                )
            )
        ],
        alignment="center"
    )

    btn_check_price= ft.Row(
        [
            ft.ElevatedButton(
                "Consultar Precio Final",
                on_click=consultar_precio_final,
                style=ft.ButtonStyle(
                    bgcolor={ft.ControlState.DEFAULT: ft.Colors.RED_600},
                    color={ft.ControlState.DEFAULT: ft.Colors.WHITE},
                    shape=ft.RoundedRectangleBorder(radius=8),
                    padding=15
                )
            )
        ],
        alignment="center"
    )

    # Evento controles dinamicos
    def on_action_change(e):
        dynamic_content.controls.clear()
        result_text.value = ""
        result_text_dict.value = None
        result_card.visible = False
        result_card_dict.visible = False

        if action_dropdown.value == "Crear Producto":
            dynamic_content.controls.extend([sku, name, base_price, currency, category, btn_create])
        elif action_dropdown.value == "Obtener Producto":
            dynamic_content.controls.extend([get_sku, btn_get])
        elif action_dropdown.value == "Listar Productos":
            dynamic_content.controls.extend([btn_list])
        elif action_dropdown.value == "Eliminar Producto":
            dynamic_content.controls.extend([delete_sku, btn_delete])
        elif action_dropdown.value == "Consultar Precio Final":
            dynamic_content.controls.extend(
                [sku, country, coupon, btn_check_price])

        page.update()

        # Contenedor dinámico
    
    dynamic_content = ft.Column(horizontal_alignment="center", spacing=10)
    
    action_dropdown.on_change = on_action_change

    # Contenedor principal
    content = ft.Container(
        content=ft.Column(
            [
                ft.Text("Gestión de Productos", size=22, weight="bold", color=ft.Colors.BLACK),
                action_dropdown, 
                dynamic_content,
                ft.Divider(),
                ft.Container(result_card, alignment=ft.alignment.center, width=400),
                ft.Container(result_card_dict, alignment=ft.alignment.center, width=400),
            ],
            horizontal_alignment="center",
            tight=True,
            spacing=15,
        ),
        bgcolor="white",
        padding=20,
        margin=20,
        border_radius=15,
        shadow=ft.BoxShadow(
            blur_radius=10, color=ft.Colors.BLACK26, offset=ft.Offset(2, 2)
        ),
        width=1000,
    )

    page.add(content)

if __name__ == "__main__":
    ft.app(
        target=main,
        view=None, 
        host="0.0.0.0", 
        port=8501 
    )
