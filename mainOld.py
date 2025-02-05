import flet as ft
from flet import Page, Row, DataTable, DataColumn, DataRow, DataCell, Column
from database import connOld

def main(page: Page):
    page.controls.clear()
    page.bgcolor = "white"
    page.title = "Cadastro de Funcionário"

    headers = connOld.tableHeader()

    #funcoes para cadastro
    def create(e):
        page.controls.clear()
        
        def register(e):
            insert = connOld.insert_user(str(dynamic_fields[0].value), str(dynamic_fields[1].value),str(dynamic_fields[2].value))
            print(insert)
            page.add(ft.Text(insert))



        dynamic_fields = [ft.TextField(label=i, width=200) for i in headers]
        dynamic_fields.append(ft.TextField(label="confirm password", width=200))
        dynamic_fields.pop(0)

        page.add(ft.Column(controls=[
            ft.Text(
                "Cadastro de Funcionário",
                size=25,  
                weight=ft.FontWeight.BOLD,  
                color="black",  
                text_align=ft.TextAlign.CENTER,  
            ),
            ft.Column(
                controls=[
                    *dynamic_fields,
                ],
                alignment=ft.MainAxisAlignment.CENTER, 
            ),
            ft.Row(
                controls=[
                    ft.ElevatedButton(text="Cadastrar", on_click=register, bgcolor="white", color="black"),
                    ft.ElevatedButton(text="Voltar", on_click=show_main_layout, bgcolor="white", color="black"),
                ],
                alignment=ft.MainAxisAlignment.CENTER
            )
        ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,  
            spacing=25,  # Espaçamento entre os elementos
            expand=True,
        ))

       
        page.update()
        
    def editar(e, id, name, email):
        page.controls.clear()
        def edit(e):
            insert = connOld.update(dynamic_fields)
            page.add(ft.Text(insert))
            get(e)


        dynamic_fields = [ft.TextField(label=i, width=100) for i in headers]
        
        dynamic_fields[0].value = id
        dynamic_fields[0].read_only=True
        dynamic_fields[1].value = name
        dynamic_fields[2].value = email 
        page.add(Row(controls=[
            *dynamic_fields,
            ft.ElevatedButton(text="Atualizar", on_click=edit),
            ft.ElevatedButton(text="Voltar", on_click=show_main_layout, bgcolor="white", color="red")
        ]))
        page.update()

    #main menu
    def show_main_layout(e):
        page.controls.clear()
        image = ft.Image(src="https://preview.redd.it/gen-1-pokemon-cassette-sleeves-legit-just-posted-the-1st-v0-sg3id3cq1ewc1.png?width=640&crop=smart&auto=webp&s=0e4291886619c7c6227ab7d09c66d70ee6f4d1d4", width=300, height=200)
        page.add(
        ft.Column(
            controls=[
                ft.Row(
                    controls=[image],
                    alignment=ft.MainAxisAlignment.CENTER
                ),
                ft.Row(
                    controls=[
                        ft.ElevatedButton(text="Cadastrar", on_click=create, bgcolor="white", color="red"),
                        ft.ElevatedButton(text="Listar", on_click=get, bgcolor="white", color="red")
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER,  
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,  
            expand=True  
        )
    )
        page.update()

    def delete_item(id, e):
            connOld.delete(id)
            print(f'Item com ID {id} deletado com sucesso!')
            get(e)
    def get(e):
        data = connOld.getAll()
        page.controls.clear()

        print(data)
        columns = [DataColumn(label=ft.Text(header)) for header in headers]        
        columns.append(DataColumn(label=ft.Text("Excluir", style="color: white; font-weight: bold")))
        columns.append(DataColumn(label=ft.Text("Editar", style="color: white; font-weight: bold")))

        rows = [
            DataRow(
                cells=[
                    *[DataCell(ft.Text(str(cell))) for cell in row],  
                    DataCell(  
                        ft.IconButton(
                            icon=ft.icons.DELETE,
                            on_click=lambda e, id=row[0]: delete_item(id, e)
                        )
                    ),
                    DataCell(  
                        ft.IconButton(
                            icon=ft.icons.EDIT,  
                            on_click=lambda e, id=row[0], name=row[1], email=row[2], password=row[3]: editar(e, id, name, email),
                        )
                    ),
                ]
            )
            for row in data
        ]

        page.add(
            Column(controls=[
                ft.ListView(
                    controls=[
                        DataTable(
                            columns=columns,
                            rows=rows,
                            width=700
                        )
                    ],
                    height=400,  
                ),
            ft.ElevatedButton(text="Voltar", on_click=show_main_layout, bgcolor="white", color="black")
        ])
        )
        page.update()
    def getPecas(e):
        data = connOld.getAllPecas()
        page.controls.clear()

        print(data)
        columns = [DataColumn(label=ft.Text(header)) for header in headers]        
        columns.append(DataColumn(label=ft.Text("Excluir", style="color: white; font-weight: bold")))
        columns.append(DataColumn(label=ft.Text("Editar", style="color: white; font-weight: bold")))

        rows = [
            DataRow(
                cells=[
                    *[DataCell(ft.Text(str(cell))) for cell in row],  
                    DataCell(  
                        ft.IconButton(
                            icon=ft.icons.DELETE,
                            on_click=lambda e, id=row[0]: delete_item(id, e)
                        )
                    ),
                    DataCell(  
                        ft.IconButton(
                            icon=ft.icons.EDIT,  
                            on_click=lambda e, id=row[0], name=row[1], email=row[2], password=row[3]: editar(e, id, name, email),
                        )
                    ),
                ]
            )
            for row in data
        ]

        page.add(
            Column(controls=[
                ft.ListView(
                    controls=[
                        DataTable(
                            columns=columns,
                            rows=rows,
                            width=700
                        )
                    ],
                    height=400,  
                ),
            ft.ElevatedButton(text="Voltar", on_click=show_main_layout, bgcolor="white", color="black")
        ])
        )
        page.update()
    # Adiciona os botões "Cadastrar" e "Listar"
    image = ft.Image(src="https://preview.redd.it/gen-1-pokemon-cassette-sleeves-legit-just-posted-the-1st-v0-sg3id3cq1ewc1.png?width=640&crop=smart&auto=webp&s=0e4291886619c7c6227ab7d09c66d70ee6f4d1d4", width=300, height=200)
    page.add(
    ft.Column(
        controls=[
            ft.Row(
                controls=[image],
                alignment=ft.MainAxisAlignment.CENTER
            ),
            ft.Row(
                controls=[
                    ft.ElevatedButton(text="Cadastrar", on_click=create, bgcolor="white", color="red"),
                    ft.ElevatedButton(text="Listar Usuarios", on_click=get, bgcolor="white", color="red"),
                    ft.ElevatedButton(text="Listar Peças", on_click=get, bgcolor="white", color="red")

                ],
                alignment=ft.MainAxisAlignment.CENTER,
            )
        ],
        alignment=ft.MainAxisAlignment.CENTER,  
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,  
        expand=True  
    )
)




    page.update()

ft.app(target=main)