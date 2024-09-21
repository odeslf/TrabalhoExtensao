import psycopg2
from psycopg2 import Error
import tkinter as tk
from tkinter import messagebox, ttk


# Conexão com o banco de dados PostgreSQL
def create_connection():
    conn = None
    try:
        conn = psycopg2.connect(
            host="localhost",  # Endereço do servidor PostgreSQL
            database="nome_do_banco_de_dados",  # Nome do banco de dados
            user="usuario",  # Seu usuário do PostgreSQL
            password="senha"  # Sua senha do PostgreSQL
        )
        return conn
    except Error as e:
        print(e)
    return conn


# Criação das tabelas Fabrica e Pedido
def create_tables(conn):
    try:
        sql_create_fabrica_table = """
        CREATE TABLE IF NOT EXISTS Fabrica (
            id_fabrica SERIAL PRIMARY KEY,
            nome VARCHAR(255) NOT NULL,
            telefone VARCHAR(20) NOT NULL
        );
        """

        sql_create_pedido_table = """
        CREATE TABLE IF NOT EXISTS Pedido (
            id_pedido SERIAL PRIMARY KEY,
            id_fabrica INTEGER NOT NULL,
            quantidade_pecas INTEGER NOT NULL,
            preco_por_peca NUMERIC(10, 2) NOT NULL,
            data_pedido DATE NOT NULL,
            FOREIGN KEY (id_fabrica) REFERENCES Fabrica (id_fabrica)
        );
        """

        cur = conn.cursor()
        cur.execute(sql_create_fabrica_table)
        cur.execute(sql_create_pedido_table)
        conn.commit()
    except Error as e:
        print(e)


# Função para inserir nova fábrica
def inserir_fabrica(conn, nome, telefone):
    sql = ''' INSERT INTO Fabrica(nome, telefone)
              VALUES(%s,%s) RETURNING id_fabrica; '''
    cur = conn.cursor()
    cur.execute(sql, (nome, telefone))
    conn.commit()
    return cur.fetchone()[0]


# Função para inserir novo pedido
def inserir_pedido(conn, id_fabrica, quantidade_pecas, preco_por_peca, data_pedido):
    sql = ''' INSERT INTO Pedido(id_fabrica, quantidade_pecas, preco_por_peca, data_pedido)
              VALUES(%s,%s,%s,%s) RETURNING id_pedido; '''
    cur = conn.cursor()
    cur.execute(sql, (id_fabrica, quantidade_pecas, preco_por_peca, data_pedido))
    conn.commit()
    return cur.fetchone()[0]


# Função para visualizar pedidos
def visualizar_pedidos(conn):
    cur = conn.cursor()
    cur.execute(
        "SELECT P.id_pedido, F.nome, P.quantidade_pecas, P.preco_por_peca, P.data_pedido FROM Pedido P JOIN Fabrica F ON P.id_fabrica = F.id_fabrica")
    rows = cur.fetchall()
    return rows


# Interface Gráfica usando Tkinter
def gui_application():
    def adicionar_fabrica():
        nome = entry_nome_fabrica.get()
        telefone = entry_telefone_fabrica.get()
        if nome and telefone:
            inserir_fabrica(conn, nome, telefone)
            messagebox.showinfo("Sucesso", "Fábrica adicionada com sucesso!")
            entry_nome_fabrica.delete(0, tk.END)
            entry_telefone_fabrica.delete(0, tk.END)
        else:
            messagebox.showerror("Erro", "Todos os campos devem ser preenchidos.")

    def adicionar_pedido():
        try:
            id_fabrica = int(entry_id_fabrica.get())
            quantidade = int(entry_quantidade_pecas.get())
            preco = float(entry_preco_por_peca.get())
            data = entry_data_pedido.get()
            inserir_pedido(conn, id_fabrica, quantidade, preco, data)
            messagebox.showinfo("Sucesso", "Pedido adicionado com sucesso!")
            entry_id_fabrica.delete(0, tk.END)
            entry_quantidade_pecas.delete(0, tk.END)
            entry_preco_por_peca.delete(0, tk.END)
            entry_data_pedido.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Erro", "Verifique os valores inseridos.")

    def exibir_pedidos():
        pedidos = visualizar_pedidos(conn)
        pedidos_tree.delete(*pedidos_tree.get_children())
        for pedido in pedidos:
            pedidos_tree.insert("", tk.END, values=pedido)

    # Conexão com o banco de dados
    conn = create_connection()
    create_tables(conn)

    # Criação da interface principal
    root = tk.Tk()
    root.title("Gestão de Pedidos")

    # Frame para Adicionar Fábrica
    frame_fabrica = tk.LabelFrame(root, text="Adicionar Fábrica")
    frame_fabrica.grid(row=0, column=0, padx=10, pady=10)

    tk.Label(frame_fabrica, text="Nome:").grid(row=0, column=0, padx=5, pady=5)
    entry_nome_fabrica = tk.Entry(frame_fabrica)
    entry_nome_fabrica.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(frame_fabrica, text="Telefone:").grid(row=1, column=0, padx=5, pady=5)
    entry_telefone_fabrica = tk.Entry(frame_fabrica)
    entry_telefone_fabrica.grid(row=1, column=1, padx=5, pady=5)

    btn_add_fabrica = tk.Button(frame_fabrica, text="Adicionar Fábrica", command=adicionar_fabrica)
    btn_add_fabrica.grid(row=2, columnspan=2, pady=10)

    # Frame para Adicionar Pedido
    frame_pedido = tk.LabelFrame(root, text="Adicionar Pedido")
    frame_pedido.grid(row=1, column=0, padx=10, pady=10)

    tk.Label(frame_pedido, text="ID Fábrica:").grid(row=0, column=0, padx=5, pady=5)
    entry_id_fabrica = tk.Entry(frame_pedido)
    entry_id_fabrica.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(frame_pedido, text="Quantidade de Peças:").grid(row=1, column=0, padx=5, pady=5)
    entry_quantidade_pecas = tk.Entry(frame_pedido)
    entry_quantidade_pecas.grid(row=1, column=1, padx=5, pady=5)

    tk.Label(frame_pedido, text="Preço por Peça:").grid(row=2, column=0, padx=5, pady=5)
    entry_preco_por_peca = tk.Entry(frame_pedido)
    entry_preco_por_peca.grid(row=2, column=1, padx=5, pady=5)

    tk.Label(frame_pedido, text="Data do Pedido:").grid(row=3, column=0, padx=5, pady=5)
    entry_data_pedido = tk.Entry(frame_pedido)
    entry_data_pedido.grid(row=3, column=1, padx=5, pady=5)

    btn_add_pedido = tk.Button(frame_pedido, text="Adicionar Pedido", command=adicionar_pedido)
    btn_add_pedido.grid(row=4, columnspan=2, pady=10)

    # Frame para Visualizar Pedidos
    frame_visualizar = tk.LabelFrame(root, text="Pedidos")
    frame_visualizar.grid(row=0, column=1, rowspan=2, padx=10, pady=10)

    pedidos_tree = ttk.Treeview(frame_visualizar, columns=("id_pedido", "nome_fabrica", "quantidade", "preco", "data"),
                                show="headings")
    pedidos_tree.heading("id_pedido", text="ID Pedido")
    pedidos_tree.heading("nome_fabrica", text="Fábrica")
    pedidos_tree.heading("quantidade", text="Quantidade")
    pedidos_tree.heading("preco", text="Preço/Peça")
    pedidos_tree.heading("data", text="Data")
    pedidos_tree.pack(fill="both", expand=True)

    btn_exibir_pedidos = tk.Button(frame_visualizar, text="Exibir Pedidos", command=exibir_pedidos)
    btn_exibir_pedidos.pack(pady=10)

    root.mainloop()


# Executar a interface gráfica
gui_application()
