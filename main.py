#para instalar o mysql connector: pip install mysql-connector-python
#bcript para criptografar: pip install bcrypt

import mysql.connector
import os

conn = mysql.connector.connect(
    host="localhost",
    port="3307",
    user="root",
    password="kapow@pass",
    database="kapowsys",
)

cursor = conn.cursor()

def verifica_conexao():
    if conn.is_connected():
        print("Conectado ao banco de dados.")
    else:
        print("Erro ao conectar ao banco de dados.")

def listar_tabelas():
    cursor.execute("SHOW TABLES")
    for tabela in cursor:
        print(tabela)

def listar_categoria_peca():
    cursor.execute("SELECT * FROM categoriaPeca")
    for categoria in cursor:
        print(categoria)

def inserir_peca(codigo_peca, nome, preco, categoriaPeca_id):
    cursor.execute("INSERT INTO peca (codigo_peca, nome, preco, categoriaPeca_id) VALUES (%s, %s, %s, %s)",
                   (codigo_peca, nome, preco, categoriaPeca_id))
    conn.commit()
    print("Peça inserida com sucesso!")

def listar_peca():
    cursor.execute("SELECT * FROM peca")
    for peca in cursor:
        print(peca)

def inserir_cliente(codigo_cliente, nome, email, senha, endereco, telefone, cpf):
    cursor.execute(
        "INSERT INTO cliente (codigo_cliente, nome, email, senha, endereco, telefone, cpf) VALUES (%s, %s, %s, %s, %s, %s, %s)",
        (codigo_cliente, nome, email, senha, endereco, telefone, cpf))
    conn.commit()
    print("Cliente inserido com sucesso!")

def listar_cliente():
    cursor.execute("SELECT * FROM cliente")
    for cliente in cursor:
        print(cliente)

def inserir_funcionario(codigo_funcionario, nome, email, endereco, telefone, cpf, salario, cargo):
    cursor.execute(
        "INSERT INTO funcionario (codigo_funcionario, nome, email, endereco, telefone, cpf, salario, cargo) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
        (codigo_funcionario, nome, email, endereco, telefone, cpf, salario, cargo))
    conn.commit()
    print("Funcionário inserido com sucesso!")

def listar_funcionario():
    cursor.execute("SELECT * FROM funcionario")
    for funcionario in cursor:
        print(funcionario)

def listar_pecas_por_categoria():
    cursor.execute("""
        SELECT c.nome AS categoria, p.id_peca, p.nome, p.preco
        FROM peca p
        JOIN categoriaPeca c ON p.categoriaPeca_id = c.id_categoriaPeca
        ORDER BY c.nome, p.nome
    """)
    pecas = cursor.fetchall()

    categoria_atual = None
    for peca in pecas:
        categoria, peca_id, nome, preco = peca
        if categoria != categoria_atual:
            print(f"\nCategoria: {categoria}")
            categoria_atual = categoria
        print(f"  {peca_id} - {nome} (R$ {preco:.2f})")

def inserir_build(codigo_build, cliente_id, funcionario_id):
    pecas_selecionadas = []
    valor_total = 0

    while True:
        listar_pecas_por_categoria()

        peca_id = input("\nDigite o código da peça (ou '0' para finalizar): ")
        if peca_id == '0':
            break

        quantidade = int(input("Digite a quantidade: "))

        cursor.execute("SELECT preco FROM peca WHERE id_peca = %s", (peca_id,))
        resultado = cursor.fetchone()

        if resultado:
            preco_unitario = resultado[0]
            valor_total += preco_unitario * quantidade
            pecas_selecionadas.append((peca_id, quantidade))
        else:
            print("Peça inválida. Tente novamente.")

    if not pecas_selecionadas:
        print("Nenhuma peça foi adicionada. Cancelando a construção da build.")
        return

    cursor.execute(
        "INSERT INTO build (codigo_build, valor, cliente_id, funcionario_id) VALUES (%s, %s, %s, %s)",
        (codigo_build, valor_total, cliente_id, funcionario_id)
    )
    conn.commit()
    build_id = cursor.lastrowid

    for peca_id, quantidade in pecas_selecionadas:
        inserir_build_peca(build_id, peca_id, quantidade)

    print(f"Build construída com sucesso! Valor total: R$ {valor_total:.2f}")

def inserir_build_peca(build_id, peca_id, quantidade):
    cursor.execute("INSERT INTO buildPeca (build_id, peca_id, quantidade) VALUES (%s, %s, %s)",
                   (build_id, peca_id, quantidade))
    conn.commit()

def listar_build():
    cursor.execute("""
        SELECT b.id_build AS build_id, p.id_peca AS peca_id, p.nome AS peca_nome, p.preco AS peca_preco, 
        SUM(p.preco) OVER (PARTITION BY b.id_build) AS valor_total_build FROM build b 
        JOIN buildpeca bp ON b.id_build = bp.build_id 
        JOIN peca p ON bp.peca_id = p.id_peca 
        ORDER BY b.id_build, p.id_peca;
        """
    )
    for build in cursor:
        print(build)

def listar_pecas_build(build_id):
    cursor.execute("""
        SELECT bp.peca_id, p.nome, bp.quantidade, p.preco, (bp.quantidade * p.preco) AS total 
        FROM buildPeca bp
        JOIN peca p ON bp.peca_id = p.id_peca
        WHERE bp.build_id = %s
        ORDER BY p.nome;
    """, (build_id,))

    pecas = cursor.fetchall()

    if not pecas:
        print(f"Nenhuma peça encontrada para a build {build_id}.")
        return []

    print(f"\nPeças da build {build_id}:")
    for peca in pecas:
        print(
            f"ID: {peca[0]}, Nome: {peca[1]}, Quantidade: {peca[2]}, Preço Unitário: R$ {peca[3]:.2f}, Total: R$ {peca[4]:.2f}")

    return pecas

def remover_peca_build(build_id, peca_id):
    cursor.execute(
        "SELECT quantidade, p.preco FROM buildPeca bp JOIN peca p ON bp.peca_id = p.id_peca WHERE bp.build_id = %s AND bp.peca_id = %s",
        (build_id, peca_id))
    resultado = cursor.fetchone()

    if not resultado:
        print("Peça não encontrada na build.")
        return

    quantidade, preco = resultado
    valor_removido = quantidade * preco

    cursor.execute("DELETE FROM buildPeca WHERE build_id = %s AND peca_id = %s", (build_id, peca_id))

    cursor.execute("UPDATE build SET valor = valor - %s WHERE id_build = %s", (valor_removido, build_id))

    conn.commit()
    print(f"Peça {peca_id} removida da build {build_id}. Valor total atualizado.")

def atualizar_quantidade_peca(build_id, peca_id, nova_quantidade):
    nova_quantidade = int(nova_quantidade)
    if nova_quantidade <= 0:
        print("Quantidade inválida. Use 'remover_peca_build' para remover a peça.")
        return

    cursor.execute(
        "SELECT quantidade, p.preco FROM buildPeca bp JOIN peca p ON bp.peca_id = p.id_peca WHERE bp.build_id = %s AND bp.peca_id = %s",
        (build_id, peca_id))
    resultado = cursor.fetchone()

    if not resultado:
        print("Peça não encontrada na build.")
        return

    quantidade_atual, preco = resultado
    diferenca_valor = (nova_quantidade - quantidade_atual) * preco

    cursor.execute("UPDATE buildPeca SET quantidade = %s WHERE build_id = %s AND peca_id = %s",
                   (nova_quantidade, build_id, peca_id))
    cursor.execute("UPDATE build SET valor = valor + %s WHERE id_build = %s", (diferenca_valor, build_id))

    conn.commit()
    print(f"Quantidade da peça {peca_id} atualizada para {nova_quantidade}. Valor total ajustado.")

def remover_build(build_id):
    cursor.execute("DELETE FROM build WHERE id_build = %s", (build_id,))
    conn.commit()
    print(f"Build {build_id} removida com sucesso.")

def listar_pecas_disponiveis():
    cursor.execute("SELECT id_peca, nome, preco FROM peca ORDER BY nome")
    pecas = cursor.fetchall()
    print("\nItens disponíveis:")
    for peca in pecas:
        peca_id, nome, preco = peca
        print(f"{peca_id} - {nome} (R$ {preco:.2f})")

def inserir_pedido_cliente(codigo_pedidoCliente, data, hora, cliente_id, funcionario_id):
    cursor.execute(
        "INSERT INTO pedidoCliente (codigo_pedidoCliente, data, hora, cliente_id, funcionario_id) VALUES (%s, %s, %s, %s, %s)",
        (codigo_pedidoCliente, data, hora, cliente_id, funcionario_id)
    )
    conn.commit()

    pedidoCliente_id = cursor.lastrowid

    while True:
        listar_pecas_disponiveis()

        item_type = input("\nDigite o tipo de item ('peca' ou 'build') ou '0' para finalizar: ").lower()

        if item_type == '0':
            break

        if item_type not in ['peca', 'build']:
            print("Tipo de item inválido. Tente novamente.")
            continue

        if item_type == 'peca':
            peca_id = input("Digite o código da peça: ")
            quantidade = int(input("Digite a quantidade da peça: "))
            inserir_item_pedido(codigo_itemPedido=None, quantidade=quantidade, pedidoCliente_id=pedidoCliente_id, peca_id=peca_id)

        elif item_type == 'build':
            build_id = input("Digite o código da build: ")
            quantidade = int(input("Digite a quantidade da build: "))
            inserir_item_pedido(codigo_itemPedido=None, quantidade=quantidade, pedidoCliente_id=pedidoCliente_id, build_id=build_id)

    while True:
        adicionar_pagamento = input("\nDeseja adicionar um pagamento ao pedido? (s/n): ").lower()
        if adicionar_pagamento == 's':
            codigo_pagamento = input("Digite o código do pagamento: ")
            valorPago = float(input("Digite o valor pago: "))
            dataPagamento = input("Digite a data do pagamento (formato: yyyy-mm-dd hh:mm:ss): ")
            metodo = input("Digite o método de pagamento (ex: Cartão, Pix, Boleto): ")
            status = input("Digite o status do pagamento (P para pago, A para aguardando): ")
            inserir_pagamento(codigo_pagamento, valorPago, dataPagamento, metodo, status, pedidoCliente_id)
        elif adicionar_pagamento == 'n':
            break
        else:
            print("Opção inválida. Tente novamente.")

    print("Pedido do cliente inserido com sucesso!")

def inserir_item_pedido(codigo_itemPedido, quantidade, pedidoCliente_id, peca_id=None, build_id=None):
    cursor.execute(
        "INSERT INTO itemPedido (codigo_itemPedido, quantidade, pedidoCliente_id, peca_id, build_id) VALUES (%s, %s, %s, %s, %s)",
        (codigo_itemPedido, quantidade, pedidoCliente_id, peca_id, build_id)
    )
    conn.commit()
    print(f"Item do pedido inserido com sucesso! Quantidade: {quantidade}")

def inserir_pagamento(codigo_pagamento, valorPago, dataPagamento, metodo, status, pedidoCliente_id):
    cursor.execute(
        "INSERT INTO pagamento (codigo_pagamento, valorPago, dataPagamento, metodo, status, pedidoCliente_id) VALUES (%s, %s, %s, %s, %s, %s)",
        (codigo_pagamento, valorPago, dataPagamento, metodo, status, pedidoCliente_id))
    conn.commit()
    print(f"Pagamento inserido com sucesso! Valor: {valorPago}, Método: {metodo}, Status: {status}")

def listar_pedido_cliente_com_itens_e_pagamento():
    cursor.execute("""
        SELECT pc.codigo_pedidoCliente, pc.data, pc.hora, pc.cliente_id, pc.funcionario_id, 
               ip.codigo_itemPedido, ip.quantidade, ip.peca_id, ip.build_id, 
               p.codigo_pagamento, p.valorPago, p.dataPagamento, p.metodo, p.status
        FROM pedidoCliente pc
        LEFT JOIN itemPedido ip ON pc.codigo_pedidoCliente = ip.pedidoCliente_id
        LEFT JOIN pagamento p ON pc.codigo_pedidoCliente = p.pedidoCliente_id
        ORDER BY pc.codigo_pedidoCliente
    """)

    pedidos = cursor.fetchall()

    if not pedidos:
        print("Nenhum pedido encontrado.")
        return

    pedidos_dict = {}

    for pedido in pedidos:
        pedido_id = pedido[0]

        if pedido_id not in pedidos_dict:
            pedidos_dict[pedido_id] = {
                'codigo_pedidoCliente': pedido[0],
                'data': pedido[1],
                'hora': pedido[2],
                'cliente_id': pedido[3],
                'funcionario_id': pedido[4],
                'itens': [],
                'pagamentos': []
            }

        # Adicionando item ao pedido
        if pedido[5] is not None:
            item = {
                'codigo_itemPedido': pedido[5],
                'quantidade': pedido[6],
                'peca_id': pedido[7],
                'build_id': pedido[8]
            }
            pedidos_dict[pedido_id]['itens'].append(item)

        # Adicionando pagamento ao pedido
        if pedido[9] is not None:
            pagamento = {
                'codigo_pagamento': pedido[9],
                'valorPago': pedido[10],
                'dataPagamento': pedido[11],
                'metodo': pedido[12],
                'status': pedido[13]
            }
            pedidos_dict[pedido_id]['pagamentos'].append(pagamento)

    # Exibindo os pedidos com itens e pagamentos
    for pedido_id, pedido_info in pedidos_dict.items():
        print(f"\nPedido {pedido_info['codigo_pedidoCliente']} (Cliente ID: {pedido_info['cliente_id']})")
        print(f"Data: {pedido_info['data']} | Hora: {pedido_info['hora']}")
        print(f"Atendido por: {pedido_info['funcionario_id']}")

        if pedido_info['itens']:
            print("Itens no pedido:")
            for item in pedido_info['itens']:
                peca_str = f"Peça ID: {item['peca_id']}" if item['peca_id'] else f"Build ID: {item['build_id']}"
                print(f"  - Item {item['codigo_itemPedido']} | Quantidade: {item['quantidade']} | {peca_str}")
        else:
            print("Nenhum item no pedido.")

        if pedido_info['pagamentos']:
            print("Pagamentos realizados:")
            for pagamento in pedido_info['pagamentos']:
                print(f"  - Pagamento ID: {pagamento['codigo_pagamento']} | Valor: {pagamento['valorPago']} | Método: {pagamento['metodo']} | Status: {pagamento['status']} | Data: {pagamento['dataPagamento']}")
        else:
            print("Nenhum pagamento realizado.")

def inserir_estoque_com_movimentacao(codigo_estoque, quantidade_estoque, peca_id, codigo_movimentacaoEstoque,
                                     quantidade_movimentacao, dataMovimentacao):
    try:
        cursor.execute(
            "INSERT INTO estoque (codigo_estoque, quantidade, peca_id) VALUES (%s, %s, %s)",
            (codigo_estoque, quantidade_estoque, peca_id)
        )
        conn.commit()
        print("Estoque inserido com sucesso!")

        cursor.execute(
            "INSERT INTO movimentacaoEstoque (codigo_movimentacaoEstoque, quantidade, dataMovimentacao, peca_id, estoque_id) VALUES (%s, %s, %s, %s, %s)",
            (codigo_movimentacaoEstoque, quantidade_movimentacao, dataMovimentacao, peca_id, codigo_estoque)
        )
        conn.commit()
        print("Movimentação de estoque inserida com sucesso!")

    except Exception as e:
        conn.rollback()
        print(f"Ocorreu um erro: {e}")


def inserir_estoque_com_movimentacao(codigo_estoque, quantidade, peca_id, codigo_movimentacaoEstoque, quantidade_movimentacao, dataMovimentacao):
    cursor.execute("SELECT id_estoque FROM estoque WHERE codigo_estoque = %s", (codigo_estoque,))
    estoque_existe = cursor.fetchone()

    if not estoque_existe:
        print("Erro: Estoque não encontrado. Inserindo novo estoque.")
        cursor.execute("INSERT INTO estoque (codigo_estoque, quantidade, peca_id) VALUES (%s, %s, %s)",
                       (codigo_estoque, quantidade, peca_id))
        conn.commit()
        print("Estoque inserido com sucesso!")

    else:
        print("Estoque encontrado, atualizando quantidade.")

        cursor.execute("UPDATE estoque SET quantidade = quantidade + %s WHERE codigo_estoque = %s",
                       (quantidade, codigo_estoque))
        conn.commit()
        print("Quantidade do estoque atualizada!")

    cursor.execute("SELECT id_estoque FROM estoque WHERE codigo_estoque = %s", (codigo_estoque,))
    estoque_id = cursor.fetchone()[0]

    cursor.execute(
        "INSERT INTO movimentacaoEstoque (codigo_movimentacaoEstoque, quantidade, dataMovimentacao, peca_id, estoque_id) VALUES (%s, %s, %s, %s, %s)",
        (codigo_movimentacaoEstoque, quantidade_movimentacao, dataMovimentacao, peca_id, estoque_id))
    conn.commit()
    print("Movimentação de estoque inserida com sucesso!")

def listar_movimentacao_estoque():
    cursor.execute("""
        SELECT m.codigo_movimentacaoEstoque, m.quantidade, m.dataMovimentacao, p.nome AS peca_nome
        FROM movimentacaoEstoque m
        JOIN peca p ON m.peca_id = p.id_peca
        ORDER BY m.dataMovimentacao
    """)
    for row in cursor:
        print(f"Movimentação Código: {row[0]}, Quantidade: {row[1]}, Data: {row[2]}, Peça: {row[3]}")

def inserir_fornecedor(codigo_fornecedor, nome, email, endereco, telefone, cnpj, pecas_ids):
    cursor.execute(
        "INSERT INTO fornecedor (codigo_fornecedor, nome, email, endereco, telefone, cnpj) VALUES (%s, %s, %s, %s, %s, %s)",
        (codigo_fornecedor, nome, email, endereco, telefone, cnpj))
    conn.commit()
    print("Fornecedor inserido com sucesso!")

    cursor.execute("SELECT id_fornecedor FROM fornecedor WHERE codigo_fornecedor = %s", (codigo_fornecedor,))
    fornecedor_id = cursor.fetchone()[0]

    for peca_id in pecas_ids:
        inserir_fornecedor_peca(fornecedor_id, peca_id)

    print("Fornecedor e suas peças associadas inseridos com sucesso!")

def inserir_fornecedor_peca(fornecedor_id, peca_id):
    cursor.execute("INSERT INTO fornecedorPeca (fornecedor_id, peca_id) VALUES (%s, %s)",
                   (fornecedor_id, peca_id))
    conn.commit()
    print(f"Peça {peca_id} associada ao fornecedor {fornecedor_id} com sucesso!")

def listar_fornecedor():
    cursor.execute("""
        SELECT f.id_fornecedor, f.nome AS fornecedor_nome, f.cnpj, p.id_peca, p.nome AS peca_nome
        FROM fornecedor f
        LEFT JOIN fornecedorPeca fp ON f.id_fornecedor = fp.fornecedor_id
        LEFT JOIN peca p ON fp.peca_id = p.id_peca
        ORDER BY f.id_fornecedor, p.id_peca;
    """)
    fornecedor_atual = None
    for fornecedor in cursor:
        if fornecedor_atual != fornecedor[0]:
            if fornecedor_atual is not None:
                print()
            fornecedor_atual = fornecedor[0]
            print(f"Fornecedor: {fornecedor[1]} (CNPJ: {fornecedor[2]})")

        if fornecedor[3] is not None:
            print(f"  Peça: {fornecedor[4]} (ID: {fornecedor[3]})")
        else:
            print(f"  Nenhuma peça associada.")

def voltar_menu():
    input("Pressione qualquer tecla para voltar ao menu principal...")

def consultar_pedido_cliente():
    query = """
        SELECT 
            pc.codigo_pedidoCliente AS pedido_codigo,
            c.nome AS cliente_nome,
            f.nome AS funcionario_nome,
            pc.data,
            pc.hora
        FROM 
            pedidoCliente pc
        JOIN cliente c ON pc.cliente_id = c.id_cliente
        JOIN funcionario f ON pc.funcionario_id = f.id_funcionario;
    """
    cursor.execute(query)
    resultados = cursor.fetchall()
    for row in resultados:
        print(f"Pedido {row[0]} - Cliente: {row[1]} - Funcionário: {row[2]} - Data: {row[3]} - Hora: {row[4]}")

def consultar_pedido_com_pecas():
    query = """
        SELECT 
            ip.codigo_itemPedido AS item_codigo,
            p.nome AS peca_nome,
            ip.quantidade
        FROM 
            itemPedido ip
        JOIN peca p ON ip.peca_id = p.id_peca;
    """
    cursor.execute(query)
    resultados = cursor.fetchall()
    for row in resultados:
        print(f"Item {row[0]} - Peça: {row[1]} - Quantidade: {row[2]}")
    cursor.close()
    conn.close()

def consultar_pagamentos_com_cliente():
    query = """
        SELECT 
            pg.codigo_pagamento AS pagamento_codigo,
            pg.valorPago,
            pg.metodo,
            pg.status,
            c.nome AS cliente_nome
        FROM 
            pagamento pg
        JOIN pedidoCliente pc ON pg.pedidoCliente_id = pc.id_pedidoCliente
        JOIN cliente c ON pc.cliente_id = c.id_cliente;
    """
    cursor.execute(query)
    resultados = cursor.fetchall()
    for row in resultados:
        print(f"Pagamento {row[0]} - Valor: {row[1]} - Método: {row[2]} - Status: {row[3]} - Cliente: {row[4]}")

# Função para consultar builds com informações da peça
def consultar_builds_com_peca():
    query = """
        SELECT 
            b.codigo_build AS build_codigo,
            p.nome AS peca_nome,
            bp.quantidade
        FROM 
            build b
        JOIN buildPeca bp ON b.id_build = bp.build_id
        JOIN peca p ON p.peca_id = p.id_peca;
    """
    cursor.execute(query)
    resultados = cursor.fetchall()
    for row in resultados:
        print(f"Build {row[0]} - Peça: {row[1]} - Quantidade: {row[2]}")

def relatorio_pedidos(data_inicial, data_final):
    query = "SELECT * FROM pedidoCliente WHERE data BETWEEN %s AND %s;"
    cursor.execute(query, (data_inicial, data_final))
    pedidos = cursor.fetchall()

    print("\nRelatório de Pedidos:")
    for pedido in pedidos:
        print(pedido)

def relatorio_pagamentos(data_inicial, data_final):
    query = "SELECT * FROM pagamento WHERE dataPagamento BETWEEN %s AND %s;"
    cursor.execute(query, (data_inicial, data_final))
    pagamentos = cursor.fetchall()

    print("\nRelatório de Pagamentos:")
    for pagamento in pagamentos:
        print(pagamento)

def relatorio_movimentacao_estoque(data_inicial, data_final):
    query = "SELECT * FROM movimentacaoEstoque WHERE dataMovimentacao BETWEEN %s AND %s;"
    cursor.execute(query, (data_inicial, data_final))
    movimentacoes = cursor.fetchall()

    print("\nRelatório de Movimentação de Estoque:")
    for movimentacao in movimentacoes:
        print(movimentacao)

def relatorio_estoque_por_categoria():
    query = """
        SELECT cp.nome AS categoria, SUM(e.quantidade) AS total_em_estoque
        FROM estoque e
        JOIN peca p ON e.peca_id = p.id_peca
        JOIN categoriaPeca cp ON p.categoriaPeca_id = cp.id_categoriaPeca
        GROUP BY cp.nome
        ORDER BY total_em_estoque DESC;
    """
    cursor.execute(query)
    categorias = cursor.fetchall()

    print("\nRelatório de Estoque por Categoria:")
    for categoria in categorias:
        print(categoria)

def relatorio_gastos_clientes(limiteInferior,limiteSuperior):
    query = """
        SELECT c.nome AS cliente, SUM(pag.valorPago) AS total_gasto
        FROM pagamento pag
        JOIN pedidoCliente pc ON pag.pedidoCliente_id = pc.id_pedidoCliente
        JOIN cliente c ON pc.cliente_id = c.id_cliente
        WHERE pag.status = 'P'
        GROUP BY c.nome
        HAVING total_gasto > %f AND total_gasto < %f
        ORDER BY total_gasto DESC;
    """
    cursor.execute(query,(limiteInferior,limiteSuperior))
    clientes = cursor.fetchall()

    print("\nRelatório de Gastos dos Clientes:")
    for cliente in clientes:
        print(cliente)

def relatorio_pedidos_funcionarios(limiteInferior,limiteSuperior):
    query = """
        SELECT f.nome AS funcionario, COUNT(pc.id_pedidoCliente) AS total_pedidos
        FROM pedidoCliente pc
        JOIN funcionario f ON pc.funcionario_id = f.id_funcionario
        GROUP BY f.nome
        HAVING total_pedidos > %f AND total_pedidos < %f
        ORDER BY total_pedidos DESC;
    """
    cursor.execute(query,(limiteInferior,limiteSuperior))
    funcionarios = cursor.fetchall()

    print("\nRelatório de Pedidos por Funcionário:")
    for funcionario in funcionarios:
        print(funcionario)

def relatorio_funcionarios_vendas_media():
    query = """
        SELECT f.nome AS funcionario, AVG(pag.valorPago) AS media_vendas
        FROM pagamento pag
        JOIN pedidoCliente pc ON pag.pedidoCliente_id = pc.id_pedidoCliente
        JOIN funcionario f ON pc.funcionario_id = f.id_funcionario
        WHERE pag.status = 'P'
        GROUP BY f.nome
        ORDER BY media_vendas DESC;
    """
    cursor.execute(query)
    funcionarios = cursor.fetchall()

    print("\nRelatório de Média de Vendas por Funcionário:")
    for funcionario in funcionarios:
        print(funcionario)

def relatorio_clientes_com_pedidos_valor(valorMinimo):
    query = """
        SELECT nome FROM cliente
        WHERE id_cliente IN (
            SELECT cliente_id FROM pedidoCliente
            WHERE id_pedidoCliente IN (
                SELECT pedidoCliente_id FROM pagamento
                WHERE valorPago > %s
            )
        );
    """
    cursor.execute(query, (valorMinimo,))
    clientes = cursor.fetchall()

    print("\nClientes com pedidos acima de", valorMinimo, ":")
    for cliente in clientes:
        print(cliente)


def relatorio_funcionarios_com_pedidos_acima_media():
    query = """
        SELECT nome FROM funcionario
        WHERE id_funcionario IN (
            SELECT funcionario_id FROM pedidoCliente
            GROUP BY funcionario_id
            HAVING COUNT(id_pedidoCliente) > (
                SELECT AVG(total_pedidos) FROM (
                    SELECT COUNT(id_pedidoCliente) AS total_pedidos FROM pedidoCliente
                    GROUP BY funcionario_id
                ) AS media_pedidos
            )
        );
    """
    cursor.execute(query)
    funcionarios = cursor.fetchall()

    print("\nFuncionários com pedidos acima da média:")
    for funcionario in funcionarios:
        print(funcionario)

def relatorio_categorias_estoque_abaixo_media():
    query = """
        SELECT nome FROM categoriaPeca
        WHERE id_categoriaPeca IN (
            SELECT categoriaPeca_id FROM peca
            WHERE id_peca IN (
                SELECT peca_id FROM estoque
                GROUP BY peca_id
                HAVING SUM(quantidade) < (
                    SELECT AVG(total_em_estoque) FROM (
                        SELECT SUM(quantidade) AS total_em_estoque FROM estoque
                        GROUP BY peca_id
                    ) AS media_estoque
                )
            )
        );
    """
    cursor.execute(query)
    categorias = cursor.fetchall()

    print("\nCategorias com estoque abaixo da média:")
    for categoria in categorias:
        print(categoria)

def main():
    op = 1
    opPeca = 0
    opPart = 0
    opBuild = 0

    while True:
        print("Digite a opção: ")
        op = input("0 - Sair\n"
                   "1 - Verificar conexão\n"
                   "2 - Listar tabelas\n"
                   "3 - Peças\n"
                   "4 - Participantes\n"
                   "5 - Builds\n"
                   "6 - Vendas\n"
                   "7 - Estoque\n"
                   "8 - Fornecedores\n"
                   "9 - Relatórios Gerenciais\n"
       )

        if op == '1':
            verifica_conexao()

        elif op == '2':
            listar_tabelas()

        elif op == '3': #Menu Pecas
            while True:
                print("Digite a opção: ")
                opPeca = input("1 - Cadastrar Categoria\n"
                           "2 - Listar Categorias\n"
                           "3 - Cadastrar Peça\n"
                           "4 - Listar Peças\n"
                           "5 - Sair\n"
                           )

                match opPeca:
                    case '1':
                        codigo_categoriaPeca = input("Digite o código da categoria da peça: ")
                        nome = input("Digite o nome da categoria da peça: ")
                        inserir_categoria_peca(codigo_categoriaPeca, nome)

                    case '2':
                        listar_categoria_peca()

                    case '3':
                        codigo_peca = input("Digite o código da peça: ")
                        nome = input("Digite o nome da peça: ")
                        preco = input("Digite o preço da peça: ")
                        categoriaPeca_id = input("Digite o id da categoria da peça: ")
                        inserir_peca(codigo_peca, nome, preco, categoriaPeca_id)

                    case '4':
                        listar_peca()

                    case '5':
                        break

        elif op == '4': # Menu Participante
            while True:
                print("Digite a opção: ")
                opPart = input("1 - Cadastrar Cliente\n"
                           "2 - Listar Clientes\n"
                           "3 - Cadastrar Funcionario\n"
                           "4 - Listar Funcionario\n"
                           "5 - Sair\n"
                           )

                match opPart:
                    case '1':
                        codigo_cliente = input("Digite o código do cliente: ")
                        nome = input("Digite o nome do cliente: ")
                        email = input("Digite o email do cliente: ")
                        senha = input("Digite a senha do cliente: ")
                        endereco = input("Digite o endereço do cliente: ")
                        telefone = input("Digite o telefone do cliente: ")
                        cpf = input("Digite o CPF do cliente: ")
                        inserir_cliente(codigo_cliente, nome, email, senha, endereco, telefone, cpf)

                    case '2':
                        listar_cliente()

                    case '3':
                        codigo_funcionario = input("Digite o código do funcionário: ")
                        nome = input("Digite o nome do funcionário: ")
                        email = input("Digite o email do funcionário: ")
                        endereco = input("Digite o endereço do funcionário: ")
                        telefone = input("Digite o telefone do funcionário: ")
                        cpf = input("Digite o CPF do funcionário: ")
                        salario = input("Digite o salário do funcionário: ")
                        cargo = input("Digite o cargo do funcionário (ex: 'A' para administrador): ")
                        inserir_funcionario(codigo_funcionario, nome, email, endereco, telefone, cpf, salario, cargo)

                    case '4':
                        listar_funcionario()

                    case '5':
                        break

        elif op == '5': # Builds
            while True:
                print("Digite a opção: ")
                opBuild = input("1 - Construir Build\n"
                                "2 - Remover Peças da Build\n"
                                "3 - Atualizar Quantidade de Peça na Build\n"
                                "4 - Remover Build\n"
                                "5 - Listar Builds\n"
                                "6 - Sair\n"
                               )

                match opBuild:
                    case '1':
                        codigo_build = input("Digite o código do build: ")
                        cliente_id = input("Digite o id do cliente: ")
                        funcionario_id = input("Digite o id do funcionário: ")
                        inserir_build(codigo_build, cliente_id, funcionario_id)

                    case '2':
                        build_id = input("Digite o código do build: ")
                        listar_pecas_build(build_id)
                        peca_id = input("Digite o id da peça que quer remover: ")
                        remover_peca_build(build_id, peca_id)

                    case '3':
                        quantidade = 0

                        build_id = input("Digite o código do build: ")
                        listar_pecas_build(build_id)
                        peca_id = input("Digite o id da peça que atualizar a quatidade: ")
                        quantidade = input("Digite a quatidade: ")
                        atualizar_quantidade_peca(build_id, peca_id, quantidade)

                    case '4':
                        build_id = input("Digite o código do build que deseja apagar: ")
                        remover_build(build_id)

                    case '5':
                        listar_build()

                    case '6':
                        break

        elif op == '6': # Vendas
            while True:
                print("Digite a opção: ")
                opVenda = input("1 - Realizar Pedido\n"
                                "2 - Listar Pedidos\n"
                                "3 - Sair\n"
                               )

                match opVenda:
                    case '1':
                        codigo_pedidoCliente = input("Digite o código do pedido do cliente: ")
                        data = input("Digite a data do pedido (formato: yyyy-mm-dd): ")
                        hora = input("Digite a hora do pedido (formato: hh:mm:ss): ")
                        cliente_id = input("Digite o id do cliente: ")
                        funcionario_id = input("Digite o id do funcionário: ")
                        inserir_pedido_cliente(codigo_pedidoCliente, data, hora, cliente_id, funcionario_id)
                    case '2':
                        listar_pedido_cliente_com_itens_e_pagamento()
                    case '3':
                        break

        elif op == '7':
            while True:
                print("Digite a opção: ")
                opEstoque = input("1 - Inserir Estoque\n"
                                "2 - Verificar Estoque\n"
                                "3 - Sair\n"
                               )

                match opEstoque:
                    case '1':
                        codigo_estoque = input("Digite o código do estoque: ")
                        quantidade = input("Digite a quantidade do estoque: ")
                        peca_id = input("Digite o id da peça: ")
                        codigo_movimentacaoEstoque = input("Digite o código da movimentação de estoque: ")
                        dataMovimentacao = input("Digite a data e hora da movimentação (formato: yyyy-mm-dd hh:mm:ss): ")
                        inserir_estoque_com_movimentacao(codigo_estoque, quantidade, peca_id, codigo_movimentacaoEstoque, quantidade, dataMovimentacao)
                    case '2':
                        listar_movimentacao_estoque()
                    case '3':
                        break

        elif op == '8':
            while True:
                peca_id = 0
                print("Digite a opção: ")
                opFornecedor = input("1 - Cadastrar Fornecedor\n"
                                  "2 - Listar Fornecedores\n"
                                  "3 - Sair\n"
                                  )

                match opFornecedor:
                    case '1':
                        codigo_fornecedor = input("Digite o código do fornecedor: ")
                        nome = input("Digite o nome do fornecedor: ")
                        email = input("Digite o email do fornecedor: ")
                        endereco = input("Digite o endereço do fornecedor: ")
                        telefone = input("Digite o telefone do fornecedor: ")
                        cnpj = input("Digite o CNPJ do fornecedor: ")

                        pecas_ids = []
                        while True:
                            peca_id = input("Digite o código da peça (ou '0' para finalizar): ")
                            if peca_id == '0':
                                break
                            pecas_ids.append(int(peca_id))

                        inserir_fornecedor(codigo_fornecedor, nome, email, endereco, telefone, cnpj, pecas_ids)
                    case '2':
                        listar_fornecedor()
                    case '3':
                        break

        elif op == '23':
            codigo_pagamento = input("Digite o código do pagamento: ")
            valorPago = input("Digite o valor pago: ")
            dataPagamento = input("Digite a data do pagamento (formato: yyyy-mm-dd hh:mm:ss): ")
            metodo = input("Digite o método de pagamento: ")
            status = input("Digite o status do pagamento (P para pago, A para aguardando): ")
            pedidoCliente_id = input("Digite o id do pedido do cliente: ")
            inserir_pagamento(codigo_pagamento, valorPago, dataPagamento, metodo, status, pedidoCliente_id)

        elif op == '24':
            listar_pagamento()

        elif op == '29':
            print("Relatórios Gerenciais")
            print("1 - Pedido por Cliente")
            print("2 - Pedidos com Peças")
            print("3 - Pagamentos com Informações do Cliente")
            print("4 - Builds com Peças")
            print("5 - Relatório de Pedidos por Data")
            print("6 - Relatório de Pagamentos por Data")
            print("7 - Relatório de Movimentação de Estoque por Data")
            print("8 - Relatório de Estoque por Categoria")
            print("9 - Relatório de Gastos dos Clientes")
            print("10 - Relatório de Pedidos por Funcionário")
            print("11 - Relatório de Média de Vendas por Funcionário")
            print("12 - Clientes com pedidos acima de valorMinimo")
            print("13 - Funcionários com pedidos acima da média")
            print("14 - Categorias com estoque abaixo da média")

            op2 = input("Escolha uma opção: ")

            if op2 == '1':
                consultar_pedido_cliente()
            elif op2 == '2':
                consultar_pedido_com_pecas()
            elif op2 == '3':
                consultar_pagamentos_com_cliente()
            elif op2 == '4':
                consultar_builds_com_peca()
            elif op2 == '5':
                data_inicial = input("Digite a data inicial (AAAA-MM-DD): ")
                data_final = input("Digite a data final (AAAA-MM-DD): ")
                relatorio_pedidos(data_inicial, data_final)
            elif op2 == '6':
                data_inicial = input("Digite a data inicial (AAAA-MM-DD): ")
                data_final = input("Digite a data final (AAAA-MM-DD): ")
                relatorio_pagamentos(data_inicial, data_final)
            elif op2 == '7':
                data_inicial = input("Digite a data inicial (AAAA-MM-DD): ")
                data_final = input("Digite a data final (AAAA-MM-DD): ")
                relatorio_movimentacao_estoque(data_inicial, data_final)
            elif op2 == '8':
                relatorio_estoque_por_categoria()
            elif op2 == '9':
                limiteInferior = input("Digite o limite inferior para os gastos")
                limiteSuperior = input("Digite o limite superior para os gastos")
                relatorio_gastos_clientes(limiteInferior,limiteSuperior)
            elif op2 == '10':
                limiteInferior = input("Digite o limite inferior para os pedidos")
                limiteSuperior = input("Digite o limite superior para os pedidos")
                relatorio_pedidos_funcionarios(limiteInferior,limiteSuperior)
            elif op2 == '11':
                relatorio_funcionarios_vendas_media()
            elif op2 == '12':
                valorMinimo = input("Digite o valor minimo para os pedidos")
                relatorio_clientes_com_pedidos_valor(valorMinimo)
            elif op2 == '13':
                relatorio_funcionarios_com_pedidos_acima_media()
            elif op2 == '14':
                relatorio_categorias_estoque_abaixo_media()
            else:
                print("Opção inválida.")

            voltar_menu()

if __name__ == "__main__":
    main()