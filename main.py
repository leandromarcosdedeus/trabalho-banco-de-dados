#para instalar o mysql connector: pip install mysql-connector-python
#bcript para criptografar: pip install bcrypt

import mysql.connector
import os

conn = mysql.connector.connect(
    host="192.168.0.190",
    port="3307",
    user="kapow_usr",
    password="kapow@pass",
    database="kapowsys",
)

cursor = conn.cursor()

def limpar_tela():
    os.system('clear')

def iniciar_tabelas():
    tabelas = [
        """
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            password VARCHAR(255) NOT NULL,
            remember_token VARCHAR(255),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            email_verified_at TIMESTAMP
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS categoriaPeca (
            id_categoriaPeca INT PRIMARY KEY AUTO_INCREMENT,
            codigo_categoriaPeca INT UNIQUE NOT NULL,
            nome VARCHAR(50) NOT NULL
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS peca (
            id_peca INT PRIMARY KEY AUTO_INCREMENT,
            codigo_peca INT UNIQUE NOT NULL,
            nome VARCHAR(50) NOT NULL,
            preco DECIMAL(10, 2) NOT NULL,
            categoriaPeca_id INT NOT NULL,
            FOREIGN KEY (categoriaPeca_id) REFERENCES categoriaPeca(id_categoriaPeca) ON DELETE CASCADE
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS cliente (
            id_cliente INT PRIMARY KEY AUTO_INCREMENT,
            codigo_cliente INT UNIQUE NOT NULL,
            nome VARCHAR(50) NOT NULL,
            email VARCHAR(50) UNIQUE NOT NULL,
            senha VARCHAR(50) NOT NULL,
            endereco VARCHAR(150) NOT NULL,
            telefone BIGINT NOT NULL,
            cpf VARCHAR(11) UNIQUE NOT NULL
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS funcionario (
            id_funcionario INT PRIMARY KEY AUTO_INCREMENT,
            codigo_funcionario INT UNIQUE NOT NULL,
            nome VARCHAR(50) NOT NULL,
            email VARCHAR(50) UNIQUE NOT NULL,
            endereco VARCHAR(150) NOT NULL,
            telefone BIGINT NOT NULL,
            cpf VARCHAR(11) UNIQUE NOT NULL,
            salario DECIMAL(10, 2) NOT NULL,
            cargo CHAR(1) NOT NULL
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS build (
            id_build INT PRIMARY KEY AUTO_INCREMENT,
            codigo_build INT UNIQUE NOT NULL,
            valor DECIMAL(10, 2) NOT NULL,
            cliente_id INT NOT NULL,
            funcionario_id INT NOT NULL,
            FOREIGN KEY (cliente_id) REFERENCES cliente(id_cliente) ON DELETE CASCADE,
            FOREIGN KEY (funcionario_id) REFERENCES funcionario(id_funcionario) ON DELETE CASCADE
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS pedidoCliente (
            id_pedidoCliente INT PRIMARY KEY AUTO_INCREMENT,
            codigo_pedidoCliente INT UNIQUE NOT NULL,
            data DATE NOT NULL,
            hora TIME NOT NULL,
            cliente_id INT NOT NULL,
            funcionario_id INT NOT NULL,
            FOREIGN KEY (cliente_id) REFERENCES cliente(id_cliente) ON DELETE CASCADE,
            FOREIGN KEY (funcionario_id) REFERENCES funcionario(id_funcionario) ON DELETE CASCADE
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS itemPedido (
            id_itemPedido INT PRIMARY KEY AUTO_INCREMENT,
            codigo_itemPedido INT UNIQUE NOT NULL,
            quantidade INT NOT NULL,
            pedidoCliente_id INT NOT NULL,
            peca_id INT DEFAULT NULL,
            build_id INT DEFAULT NULL,
            FOREIGN KEY (pedidoCliente_id) REFERENCES pedidoCliente(id_pedidoCliente) ON DELETE CASCADE,
            FOREIGN KEY (peca_id) REFERENCES peca(id_peca) ON DELETE CASCADE,
            FOREIGN KEY (build_id) REFERENCES build(id_build) ON DELETE CASCADE,
            CHECK (peca_id IS NOT NULL OR build_id IS NOT NULL)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS estoque (
            id_estoque INT PRIMARY KEY AUTO_INCREMENT,
            codigo_estoque INT UNIQUE NOT NULL,
            quantidade INT NOT NULL,
            peca_id INT NOT NULL,
            FOREIGN KEY (peca_id) REFERENCES peca(id_peca) ON DELETE CASCADE
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS movimentacaoEstoque (
            id_movimentacaoEstoque INT PRIMARY KEY AUTO_INCREMENT,
            codigo_movimentacaoEstoque INT UNIQUE NOT NULL,
            quantidade INT NOT NULL,
            dataMovimentacao DATETIME NOT NULL,
            peca_id INT NOT NULL,
            estoque_id INT NOT NULL,
            FOREIGN KEY (peca_id) REFERENCES peca(id_peca) ON DELETE CASCADE,
            FOREIGN KEY (estoque_id) REFERENCES estoque(id_estoque) ON DELETE CASCADE
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS fornecedor (
            id_fornecedor INT PRIMARY KEY AUTO_INCREMENT,
            codigo_fornecedor INT UNIQUE NOT NULL,
            nome VARCHAR(50) NOT NULL,
            email VARCHAR(50) UNIQUE NOT NULL,
            endereco VARCHAR(150) NOT NULL,
            telefone BIGINT NOT NULL,
            cnpj VARCHAR(14) UNIQUE NOT NULL
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS pagamento (
            id_pagamento INT PRIMARY KEY AUTO_INCREMENT,
            codigo_pagamento INT UNIQUE NOT NULL,
            valorPago DECIMAL(10, 2) NOT NULL,
            dataPagamento DATETIME NOT NULL,
            metodo VARCHAR(30) NOT NULL,
            status CHAR(1) NOT NULL,
            pedidoCliente_id INT NOT NULL,
            FOREIGN KEY (pedidoCliente_id) REFERENCES pedidoCliente(id_pedidoCliente) ON DELETE CASCADE
        )
        """,
        """
        CREATE TABLE buildPeca(
    id_buildPeca INT PRIMARY KEY AUTO_INCREMENT,
    build_id INT NOT NULL,
    peca_id INT NOT NULL,
    quantidade INT NOT NULL,
    FOREIGN KEY (build_id) REFERENCES build(id_build) ON DELETE CASCADE,
    FOREIGN KEY (peca_id) REFERENCES peca(id_peca) ON DELETE CASCADE
);
        """,
        """
CREATE TABLE fornecedorPeca(
    id_fornecedorPeca INT PRIMARY KEY AUTO_INCREMENT,
    fornecedor_id INT NOT NULL,
    peca_id INT NOT NULL,
    FOREIGN KEY (fornecedor_id) REFERENCES fornecedor(id_fornecedor) ON DELETE CASCADE,
    FOREIGN KEY (peca_id) REFERENCES peca(id_peca) ON DELETE CASCADE
);
        """
    ]

    for tabela in tabelas:
        cursor.execute(tabela)
        cursor.nextset()
    
    conn.commit()


def listar_tabelas():
    cursor.execute("SHOW TABLES")
    tabelas = cursor.fetchall()
    
    print("\nTabelas no banco de dados:")
    print("-" * 30)
    for tabela in tabelas:
        print(f"- {tabela[0]}")
    print("-" * 30)



def inserir_categoria_peca(codigo_categoriaPeca, nome):
    cursor.execute("INSERT INTO categoriaPeca (codigo_categoriaPeca, nome) VALUES (%s, %s)", (codigo_categoriaPeca, nome))
    conn.commit()
    print("Categoria de peça inserida com sucesso!")


def listar_categoria_peca():
    query = "SELECT id_categoriaPeca, codigo_categoriaPeca, nome FROM categoriaPeca"
    cursor.execute(query)
    
    categorias = cursor.fetchall()
    
    print("\nLista de Categorias de Peças:")
    print("{:<5} {:<15} {:<50}".format("ID", "Código", "Nome"))
    print("-" * 70)
    
    for categoria in categorias:
        print("{:<5} {:<15} {:<50}".format(categoria[0], categoria[1], categoria[2]))



def inserir_peca(codigo_peca, nome, preco, categoriaPeca_id):
    cursor.execute("INSERT INTO peca (codigo_peca, nome, preco, categoriaPeca_id) VALUES (%s, %s, %s, %s)", 
                   (codigo_peca, nome, preco, categoriaPeca_id))
    conn.commit()
    print("Peça inserida com sucesso!")


def listar_peca():
    query = """
        SELECT p.id_peca, p.codigo_peca, p.nome, p.preco, cp.nome AS categoria
        FROM peca p
        JOIN categoriaPeca cp ON p.categoriaPeca_id = cp.id_categoriaPeca
    """
    cursor.execute(query)
    pecas = cursor.fetchall()

    print("\nLista de Peças:")
    print("{:<5} {:<15} {:<30} {:<10} {:<20}".format("ID", "Código", "Nome", "Preço", "Categoria"))
    print("-" * 80)

    for peca in pecas:
        print("{:<5} {:<15} {:<30} R${:<8.2f} {:<20}".format(peca[0], peca[1], peca[2], peca[3], peca[4]))




def inserir_cliente(codigo_cliente, nome, email, senha, endereco, telefone, cpf):
    cursor.execute("INSERT INTO cliente (codigo_cliente, nome, email, senha, endereco, telefone, cpf) VALUES (%s, %s, %s, %s, %s, %s, %s)", 
                   (codigo_cliente, nome, email, senha, endereco, telefone, cpf))
    conn.commit()
    print("Cliente inserido com sucesso!")


def listar_cliente():
    query = """
        SELECT id_cliente, codigo_cliente, nome, email, endereco, telefone, cpf
        FROM cliente
    """
    cursor.execute(query)
    clientes = cursor.fetchall()

    print("\nLista de Clientes:")
    print("{:<5} {:<15} {:<30} {:<30} {:<40} {:<16} {:<11}".format(
        "ID", "Código", "Nome", "Email", "Endereço", "Telefone", "CPF"
    ))
    print("-" * 150)

    for cliente in clientes:
        print("{:<5} {:<15} {:<30} {:<30} {:<40} {:<16} {:<11}".format(
            cliente[0], cliente[1], cliente[2], cliente[3], cliente[4], cliente[5], cliente[6]
        ))



def inserir_funcionario(codigo_funcionario, nome, email, endereco, telefone, cpf, salario, cargo):
    cursor.execute("INSERT INTO funcionario (codigo_funcionario, nome, email, endereco, telefone, cpf, salario, cargo) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", 
                   (codigo_funcionario, nome, email, endereco, telefone, cpf, salario, cargo))
    conn.commit()
    print("Funcionário inserido com sucesso!")


def listar_funcionario():
    query = """
        SELECT id_funcionario, codigo_funcionario, nome, email, endereco, telefone, cpf, salario, cargo
        FROM funcionario
    """
    cursor.execute(query)
    funcionarios = cursor.fetchall()

    print("\nLista de Funcionários:")
    print("{:<5} {:<15} {:<30} {:<30} {:<40} {:<16} {:<11} {:<10} {:<5}".format(
        "ID", "Código", "Nome", "Email", "Endereço", "Telefone", "CPF", "Salário", "Cargo"
    ))
    print("-" * 170)

    for funcionario in funcionarios:
        print("{:<5} {:<15} {:<30} {:<30} {:<40} {:<16} {:<11} {:<10.2f} {:<5}".format(
            funcionario[0], funcionario[1], funcionario[2], funcionario[3], funcionario[4], 
            funcionario[5], funcionario[6], funcionario[7], funcionario[8]
        ))



def inserir_build(codigo_build, valor, cliente_id, funcionario_id):
    cursor.execute("INSERT INTO build (codigo_build, valor, cliente_id, funcionario_id) VALUES (%s, %s, %s, %s)", 
                   (codigo_build, valor, cliente_id, funcionario_id))
    conn.commit()
    print("Build inserido com sucesso!")


def listar_build():
    cursor.execute("SELECT * FROM build")
    for build in cursor:
        print(build)


def inserir_pedido_cliente(codigo_pedidoCliente, data, hora, cliente_id, funcionario_id):
    cursor.execute("INSERT INTO pedidoCliente (codigo_pedidoCliente, data, hora, cliente_id, funcionario_id) VALUES (%s, %s, %s, %s, %s)", 
                   (codigo_pedidoCliente, data, hora, cliente_id, funcionario_id))
    conn.commit()
    print("Pedido do cliente inserido com sucesso!")


def listar_pedido_cliente():
    query = """
        SELECT p.id_pedidoCliente, p.codigo_pedidoCliente, 
               DATE_FORMAT(p.data, '%d/%m/%Y') AS data_pedido, 
               TIME_FORMAT(p.hora, '%H:%i') AS hora_pedido, 
               c.nome AS cliente, f.nome AS funcionario
        FROM pedidoCliente p
        JOIN cliente c ON p.cliente_id = c.id_cliente
        JOIN funcionario f ON p.funcionario_id = f.id_funcionario
    """
    cursor.execute(query)
    pedidos = cursor.fetchall()

    print("\nLista de Pedidos dos Clientes:")
    print("{:<5} {:<15} {:<12} {:<8} {:<30} {:<30}".format(
        "ID", "Código", "Data", "Hora", "Cliente", "Funcionário"
    ))
    print("-" * 100)

    for pedido in pedidos:
        print("{:<5} {:<15} {:<12} {:<8} {:<30} {:<30}".format(
            pedido[0], pedido[1], pedido[2], pedido[3], pedido[4], pedido[5]
        ))



def inserir_item_pedido(codigo_itemPedido, quantidade, pedidoCliente_id, peca_id=None, build_id=None):
    cursor.execute("INSERT INTO itemPedido (codigo_itemPedido, quantidade, pedidoCliente_id, peca_id, build_id) VALUES (%s, %s, %s, %s, %s)", 
                   (codigo_itemPedido, quantidade, pedidoCliente_id, peca_id, build_id))
    conn.commit()
    print("Item do pedido inserido com sucesso!")


def listar_item_pedido():
    query = """
        SELECT i.id_itemPedido, i.codigo_itemPedido, i.quantidade, 
               p.codigo_pedidoCliente, 
               COALESCE(pe.nome, b.codigo_build) AS item_nome
        FROM itemPedido i
        JOIN pedidoCliente p ON i.pedidoCliente_id = p.id_pedidoCliente
        LEFT JOIN peca pe ON i.peca_id = pe.id_peca
        LEFT JOIN build b ON i.build_id = b.id_build
    """
    cursor.execute(query)
    itens = cursor.fetchall()

    print("\nLista de Itens dos Pedidos:")
    print("{:<5} {:<15} {:<10} {:<15} {:<30}".format(
        "ID", "Código", "Qtd", "Pedido", "Item (Peça/Build)"
    ))
    print("-" * 80)

    for item in itens:
        print("{:<5} {:<15} {:<10} {:<15} {:<30}".format(
            item[0], item[1], item[2], item[3], item[4]
        ))



def inserir_estoque(codigo_estoque, quantidade, peca_id):
    cursor.execute("INSERT INTO estoque (codigo_estoque, quantidade, peca_id) VALUES (%s, %s, %s)", 
                   (codigo_estoque, quantidade, peca_id))
    conn.commit()
    print("Estoque inserido com sucesso!")


def listar_estoque():
    query = """
        SELECT e.id_estoque, e.codigo_estoque, p.nome AS nome_peca, e.quantidade
        FROM estoque e
        JOIN peca p ON e.peca_id = p.id_peca
        ORDER BY p.nome;
    """
    cursor.execute(query)
    estoques = cursor.fetchall()
    
    print(f"{'ID':<5} {'Código':<10} {'Peça':<30} {'Quantidade':<10}")
    print("-" * 60)
    
    for estoque in estoques:
        print(f"{estoque[0]:<5} {estoque[1]:<10} {estoque[2]:<30} {estoque[3]:<10}")

    if not estoques:
        print("Nenhum item em estoque.")



def inserir_movimentacao_estoque(codigo_movimentacaoEstoque, quantidade, dataMovimentacao, peca_id, estoque_id):
    cursor.execute("INSERT INTO movimentacaoEstoque (codigo_movimentacaoEstoque, quantidade, dataMovimentacao, peca_id, estoque_id) VALUES (%s, %s, %s, %s, %s)", 
                   (codigo_movimentacaoEstoque, quantidade, dataMovimentacao, peca_id, estoque_id))
    conn.commit()
    print("Movimentação de estoque inserida com sucesso!")


def listar_movimentacao_estoque():
    query = """
        SELECT m.id_movimentacaoEstoque, m.codigo_movimentacaoEstoque, 
               p.nome AS nome_peca, m.quantidade, m.dataMovimentacao
        FROM movimentacaoEstoque m
        JOIN peca p ON m.peca_id = p.id_peca
        ORDER BY m.dataMovimentacao DESC;
    """
    
    cursor.execute(query)
    movimentacoes = cursor.fetchall()
    
    print(f"{'ID':<5} {'Código':<10} {'Peça':<30} {'Quantidade':<12} {'Data e Hora':<20}")
    print("-" * 80)
    
    for mov in movimentacoes:
        print(f"{mov[0]:<5} {mov[1]:<10} {mov[2]:<30} {mov[3]:<12} {mov[4]:<20}")

    if not movimentacoes:
        print("Nenhuma movimentação registrada no estoque.")



def inserir_fornecedor(codigo_fornecedor, nome, email, endereco, telefone, cnpj):
    cursor.execute("INSERT INTO fornecedor (codigo_fornecedor, nome, email, endereco, telefone, cnpj) VALUES (%s, %s, %s, %s, %s, %s)", 
                   (codigo_fornecedor, nome, email, endereco, telefone, cnpj))
    conn.commit()
    print("Fornecedor inserido com sucesso!")


def listar_fornecedor():
    query = """
        SELECT id_fornecedor, codigo_fornecedor, nome, email, telefone, cnpj
        FROM fornecedor
        ORDER BY nome;
    """
    
    cursor.execute(query)
    fornecedores = cursor.fetchall()

    print(f"{'ID':<5} {'Código':<10} {'Nome':<30} {'Email':<30} {'Telefone':<15} {'CNPJ':<15}")
    print("-" * 110)
    
    for fornecedor in fornecedores:
        print(f"{fornecedor[0]:<5} {fornecedor[1]:<10} {fornecedor[2]:<30} {fornecedor[3]:<30} {fornecedor[4]:<15} {fornecedor[5]:<15}")

    if not fornecedores:
        print("Nenhum fornecedor cadastrado.")



def inserir_pagamento(codigo_pagamento, valorPago, dataPagamento, metodo, status, pedidoCliente_id):
    cursor.execute("INSERT INTO pagamento (codigo_pagamento, valorPago, dataPagamento, metodo, status, pedidoCliente_id) VALUES (%s, %s, %s, %s, %s, %s)", 
                   (codigo_pagamento, valorPago, dataPagamento, metodo, status, pedidoCliente_id))
    conn.commit()
    print("Pagamento inserido com sucesso!")


def listar_pagamento():
    query = """
        SELECT p.id_pagamento, p.codigo_pagamento, p.valorPago, p.dataPagamento, 
               p.metodo, p.status, pc.codigo_pedidoCliente
        FROM pagamento p
        JOIN pedidoCliente pc ON p.pedidoCliente_id = pc.id_pedidoCliente
        ORDER BY p.dataPagamento DESC;
    """
    
    cursor.execute(query)
    pagamentos = cursor.fetchall()

    print(f"{'ID':<5} {'Código':<10} {'Valor Pago':<12} {'Data Pagamento':<20} {'Método':<15} {'Status':<8} {'Pedido':<10}")
    print("-" * 90)
    
    for pag in pagamentos:
        status_str = "Pago" if pag[5] == "P" else "Pendente"  # Supondo que 'P' significa "Pago"
        print(f"{pag[0]:<5} {pag[1]:<10} R${pag[2]:<10.2f} {pag[3]:<20} {pag[4]:<15} {status_str:<8} {pag[6]:<10}")

    if not pagamentos:
        print("Nenhum pagamento registrado.")



def voltar_menu():
    input("Pressione qualquer tecla para voltar ao menu principal...")

def inserir_build_peca(build_id, peca_id, quantidade):
    cursor.execute("INSERT INTO buildPeca (build_id, peca_id, quantidade) VALUES (%s, %s, %s)", 
                   (build_id, peca_id, quantidade))
    conn.commit()
    print("BuildPeca inserido com sucesso!")

def listar_build_peca():
    cursor.execute("SELECT * FROM buildPeca")
    for buildPeca in cursor:
        print(buildPeca)

def inserir_fornecedor_peca(fornecedor_id, peca_id):
    cursor.execute("INSERT INTO fornecedorPeca (fornecedor_id, peca_id) VALUES (%s, %s)", 
                   (fornecedor_id, peca_id))
    conn.commit()
    print("FornecedorPeca inserido com sucesso!")

def listar_fornecedor_peca():
    cursor.execute("SELECT * FROM fornecedorPeca")
    for fornecedorPeca in cursor:
        print(fornecedorPeca)

# Função para consultar pedidos de clientes
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

# Função para consultar pedidos com peças
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

# Função para consultar pagamentos com dados do cliente
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


# Menu principal
op = 1
while(op != '0'):
    print("Digite a opção: ")
    op = input("0 - Sair\n1 - Iniciar tabelas\n2 - Listar tabelas\n3 - Inserir categoriaPeca\n4 - Listar categoriaPeca\n5 - Inserir peca\n6 - Listar peca\n7 - Inserir cliente\n8 - Listar cliente\n9 - Inserir funcionario\n10 - Listar funcionario\n11 - Inserir build\n12 - Listar build\n13 - Inserir pedidoCliente\n14 - Listar pedidoCliente\n15 - Inserir itemPedido\n16 - Listar itemPedido\n17 - Inserir estoque\n18 - Listar estoque\n19 - Inserir movimentacaoEstoque\n20 - Listar movimentacaoEstoque\n21 - Inserir fornecedor\n22 - Listar fornecedor\n23 - Inserir pagamento\n24 - Listar pagamento\n25 - Inserir buildPeca\n26 - Listar buildPeca\n27 - Inserir fornecedorPeca\n28 - Listar fornecedorPeca\n29 - Relatórios Gerenciais\n")

    if op == '1':
        iniciar_tabelas()
        voltar_menu()

    elif op == '2':
        listar_tabelas()
        voltar_menu()

    elif op == '3':
        codigo_categoriaPeca = input("Digite o código da categoria da peça: ")
        nome = input("Digite o nome da categoria da peça: ")
        inserir_categoria_peca(codigo_categoriaPeca, nome)
        voltar_menu()

    elif op == '4':
        listar_categoria_peca()
        voltar_menu()

    elif op == '5':
        codigo_peca = input("Digite o código da peça: ")
        nome = input("Digite o nome da peça: ")
        preco = input("Digite o preço da peça: ")
        categoriaPeca_id = input("Digite o id da categoria da peça: ")
        inserir_peca(codigo_peca, nome, preco, categoriaPeca_id)
        voltar_menu()

    elif op == '6':
        listar_peca()
        voltar_menu()
    elif op == '7':
        codigo_cliente = input("Digite o código do cliente: ")
        nome = input("Digite o nome do cliente: ")
        email = input("Digite o email do cliente: ")
        senha = input("Digite a senha do cliente: ")
        endereco = input("Digite o endereço do cliente: ")
        telefone = input("Digite o telefone do cliente: ")
        cpf = input("Digite o CPF do cliente: ")
        inserir_cliente(codigo_cliente, nome, email, senha, endereco, telefone, cpf)
        voltar_menu()

    elif op == '8':
        listar_cliente()
        voltar_menu()

    elif op == '9':
        codigo_funcionario = input("Digite o código do funcionário: ")
        nome = input("Digite o nome do funcionário: ")
        email = input("Digite o email do funcionário: ")
        endereco = input("Digite o endereço do funcionário: ")
        telefone = input("Digite o telefone do funcionário: ")
        cpf = input("Digite o CPF do funcionário: ")
        salario = input("Digite o salário do funcionário: ")
        cargo = input("Digite o cargo do funcionário (ex: 'A' para administrador): ")
        inserir_funcionario(codigo_funcionario, nome, email, endereco, telefone, cpf, salario, cargo)
        voltar_menu()

    elif op == '10':
        listar_funcionario()
        voltar_menu()

    elif op == '11':
        codigo_build = input("Digite o código do build: ")
        valor = input("Digite o valor do build: ")
        cliente_id = input("Digite o id do cliente: ")
        funcionario_id = input("Digite o id do funcionário: ")
        inserir_build(codigo_build, valor, cliente_id, funcionario_id)
        voltar_menu()

    elif op == '12':
        listar_build()
        voltar_menu()

    elif op == '13':
        codigo_pedidoCliente = input("Digite o código do pedido do cliente: ")
        data = input("Digite a data do pedido (formato: yyyy-mm-dd): ")
        hora = input("Digite a hora do pedido (formato: hh:mm:ss): ")
        cliente_id = input("Digite o id do cliente: ")
        funcionario_id = input("Digite o id do funcionário: ")
        inserir_pedido_cliente(codigo_pedidoCliente, data, hora, cliente_id, funcionario_id)
        voltar_menu()

    elif op == '14':
        listar_pedido_cliente()
        voltar_menu()

    elif op == '15':
        codigo_itemPedido = input("Digite o código do item do pedido: ")
        quantidade = input("Digite a quantidade do item: ")
        pedidoCliente_id = input("Digite o id do pedido do cliente: ")
        peca_id = input("Digite o id da peça (ou pressione Enter para não informar): ")
        build_id = input("Digite o id do build (ou pressione Enter para não informar): ")
        inserir_item_pedido(codigo_itemPedido, quantidade, pedidoCliente_id, peca_id or None, build_id or None)
        voltar_menu()

    elif op == '16':
        listar_item_pedido()
        voltar_menu()

    elif op == '17':
        codigo_estoque = input("Digite o código do estoque: ")
        quantidade = input("Digite a quantidade do estoque: ")
        peca_id = input("Digite o id da peça: ")
        inserir_estoque(codigo_estoque, quantidade, peca_id)
        voltar_menu()

    elif op == '18':
        listar_estoque()

        voltar_menu()

    elif op == '19':
        codigo_movimentacaoEstoque = input("Digite o código da movimentação de estoque: ")
        quantidade = input("Digite a quantidade movimentada: ")
        dataMovimentacao = input("Digite a data e hora da movimentação (formato: yyyy-mm-dd hh:mm:ss): ")
        peca_id = input("Digite o id da peça: ")
        estoque_id = input("Digite o id do estoque: ")
        inserir_movimentacao_estoque(codigo_movimentacaoEstoque, quantidade, dataMovimentacao, peca_id, estoque_id)
        voltar_menu()

    elif op == '20':
        listar_movimentacao_estoque()
        voltar_menu()

    elif op == '21':
        codigo_fornecedor = input("Digite o código do fornecedor: ")
        nome = input("Digite o nome do fornecedor: ")
        email = input("Digite o email do fornecedor: ")
        endereco = input("Digite o endereço do fornecedor: ")
        telefone = input("Digite o telefone do fornecedor: ")
        cnpj = input("Digite o CNPJ do fornecedor: ")
        inserir_fornecedor(codigo_fornecedor, nome, email, endereco, telefone, cnpj)
        voltar_menu()

    elif op == '22':
        listar_fornecedor()
        voltar_menu()

    elif op == '23':
        codigo_pagamento = input("Digite o código do pagamento: ")
        valorPago = input("Digite o valor pago: ")
        dataPagamento = input("Digite a data do pagamento (formato: yyyy-mm-dd hh:mm:ss): ")
        metodo = input("Digite o método de pagamento: ")
        status = input("Digite o status do pagamento (P para pago, A para aguardando): ")
        pedidoCliente_id = input("Digite o id do pedido do cliente: ")
        inserir_pagamento(codigo_pagamento, valorPago, dataPagamento, metodo, status, pedidoCliente_id)
        voltar_menu()

    elif op == '24':
        listar_pagamento()
        voltar_menu()

    elif op == '25':
        build_id = input("Digite o código do build: ")
        peca_id = input("Digite o código da peça: ")
        quantidade = input("Digite a quantidade: ")
        inserir_build_peca(build_id, peca_id, quantidade)
        voltar_menu()

    elif op == '26':
        listar_build_peca()
        voltar_menu()

    elif op == '27':
        fornecedor_id = input("Digite o código do fornecedor: ")
        peca_id = input("Digite o código da peça: ")
        inserir_fornecedor_peca(fornecedor_id, peca_id)
        voltar_menu()

    elif op == '28':
        listar_fornecedor_peca()
        voltar_menu()

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

    limpar_tela()
