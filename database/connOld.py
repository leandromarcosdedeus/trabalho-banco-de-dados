#para instalar o mysql connector: pip install mysql-connector-python
#bcript para criptografar: pip install bcrypt

import mysql.connector
import bcrypt

conn = mysql.connector.connect(
    host="localhost",
    port="3306",
    user="root",
    password="root",
    database="trabalho_bd",
)

cursor = conn.cursor()


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

def tableHeader():
    cursor.execute('select * from users')
    exclude_columns = {'remember_token', 'created_at', 'updated_at', 'email_verified_at'}  
    column_names = []

    for linha in cursor.description:
        if linha[0] not in exclude_columns:  
            column_names.append(linha[0])

    cursor.nextset()

    return column_names

def getAll():
    cursor.execute('select * from users')
    results = cursor.fetchall()
    headers = tableHeader()  
    
    data = [[row[i] for i in range(len(headers))] for row in results]
    
    cursor.nextset()
    return data

def getAllPecas():
    cursor.execute('select * from peca')
    results = cursor.fetchall()
    headers = tableHeader()  
    
    data = [[row[i] for i in range(len(headers))] for row in results]
    
    cursor.nextset()
    return data

def insert_user(name, email, password):
    # Criptografar o password
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    query = """
    INSERT INTO users (name, email, password)
    VALUES (%s, %s, %s)
    """

    cursor.execute(query, (name, email, hashed_password))

    conn.commit()
    cursor.nextset()
    return "Usuário " + name+ " inserido com sucesso!"

def delete(id):
    try:
        query = "DELETE FROM users WHERE id = %s"
        cursor.execute(query, (id,))
        cursor.nextset()  
        conn.commit()  
        return "Usuário deletado com sucesso!"
    except Exception as e:
        return f"Erro ao deletar usuário: {e}"
    
def update(values):
    query = "UPDATE users SET name = %s, email = %s, password = %s WHERE id = %s"
    
    params = (values[1].value, values[2].value, values[3].value, values[0].value)

    print("Query:", query)
    print("Parâmetros:", params)
    cursor.execute(query,params)

