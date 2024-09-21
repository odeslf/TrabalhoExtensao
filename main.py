import psycopg2
import tkinter as tk
from tkinter import messagebox, ttk


def create_connection():
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="costura",
            user="postgres",
            password="Selacanto"
        )
        return conn
    except Exception as e:
        print("Erro ao conectar ao banco de dados:")
        print(e)
        return None


def create_tables(conn):
    try:
        cur = conn.cursor()

        cur.execute('''
            CREATE TABLE IF NOT EXISTS Fabrica (
                id SERIAL PRIMARY KEY,
                nome VARCHAR(255) NOT NULL,
                telefone VARCHAR(15) NOT NULL,
                endereco VARCHAR(255) NOT NULL
            )
        ''')

        cur.execute('''
            CREATE TABLE IF NOT EXISTS Pedido (
                id SERIAL PRIMARY KEY,
                fabrica_id INTEGER REFERENCES Fabrica(id),
                quantidade INTEGER NOT NULL,
                preco_por_peca NUMERIC(10, 2) NOT NULL
            )
        ''')

        conn.commit()
        cur.close()
        print("Tabelas criadas com sucesso!")
    except Exception as e:
        conn.rollback()
        print("Erro ao criar tabelas:")
        print(e)


def insert_fabrica(conn, nome, telefone, endereco):
    try:
        cur = conn.cursor()
        cur.execute("INSERT INTO Fabrica (nome, telefone, endereco) VALUES (%s, %s, %s)",
                    (nome, telefone, endereco))
        conn.commit()
        cur.close()
        print("Fábrica inserida com sucesso!")
    except Exception as e:
        conn.rollback()
        print("Erro ao inserir fábrica:")
        print(e)


def insert_pedido(conn, fabrica_id, quantidade, preco_por_peca):
    try:
        cur = conn.cursor()
        cur.execute("INSERT INTO Pedido (fabrica_id, quantidade, preco_por_peca) VALUES (%s, %s, %s)",
                    (fabrica_id, quantidade, preco_por_peca))
        conn.commit()
        cur.close()
        print("Pedido inserido com sucesso!")
    except Exception as e:
        conn.rollback()
        print("Erro ao inserir pedido:")
        print(e)


def fetch_fabricas(conn):
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM Fabrica")
        fabricas = cur.fetchall()
        cur.close()
        return fabricas
    except Exception as e:
        print("Erro ao consultar fábricas:")
        print(e)
        return []


def fetch_pedidos(conn):
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM Pedido")
        pedidos = cur.fetchall()
        cur.close()
        return pedidos
    except Exception as e:
        print("Erro ao consultar pedidos:")
        print(e)
        return []


def delete_fabrica(conn, fabrica_id):
    try:
        cur = conn.cursor()
        cur.execute("DELETE FROM Fabrica WHERE id = %s", (fabrica_id,))
        conn.commit()
        cur.close()
        print(f"Fábrica com ID {fabrica_id} removida com sucesso!")
    except Exception as e:
        conn.rollback()
        print("Erro ao remover fábrica:")
        print(e)


def delete_pedido(conn, pedido_id):
    try:
        cur = conn.cursor()
        cur.execute("DELETE FROM Pedido WHERE id = %s", (pedido_id,))
        conn.commit()
        cur.close()
        print(f"Pedido com ID {pedido_id} removido com sucesso!")
    except Exception as e:
        conn.rollback()
        print("Erro ao remover pedido:")
        print(e)


def gui_application():
    conn = create_connection()
    if conn is None:
        return

    create_tables(conn)

    root = tk.Tk()
    root.title("Sistema de Costura")

    # Frame para Inserir Fábrica
    fabrica_frame = tk.Frame(root)
    fabrica_frame.pack(padx=10, pady=10)

    tk.Label(fabrica_frame, text="Nome da Fábrica").grid(row=0, column=0)
    nome_entry = tk.Entry(fabrica_frame)
    nome_entry.grid(row=0, column=1)

    tk.Label(fabrica_frame, text="Telefone").grid(row=1, column=0)
    telefone_entry = tk.Entry(fabrica_frame)
    telefone_entry.grid(row=1, column=1)

    tk.Label(fabrica_frame, text="Endereço").grid(row=2, column=0)
    endereco_entry = tk.Entry(fabrica_frame)
    endereco_entry.grid(row=2, column=1)

    def submit_fabrica():
        nome = nome_entry.get()
        telefone = telefone_entry.get()
        endereco = endereco_entry.get()
        if nome and telefone and endereco:
            insert_fabrica(conn, nome, telefone, endereco)
            nome_entry.delete(0, tk.END)
            telefone_entry.delete(0, tk.END)
            endereco_entry.delete(0, tk.END)
            refresh_fabricas()
        else:
            messagebox.showwarning("Atenção", "Todos os campos são obrigatórios!")

    tk.Button(fabrica_frame, text="Inserir Fábrica", command=submit_fabrica).grid(row=3, columnspan=2, pady=10)

    # Frame para Inserir Pedido
    pedido_frame = tk.Frame(root)
    pedido_frame.pack(padx=10, pady=10)

    tk.Label(pedido_frame, text="Fábrica ID").grid(row=0, column=0)
    fabrica_id_entry = tk.Entry(pedido_frame)
    fabrica_id_entry.grid(row=0, column=1)

    tk.Label(pedido_frame, text="Quantidade").grid(row=1, column=0)
    quantidade_entry = tk.Entry(pedido_frame)
    quantidade_entry.grid(row=1, column=1)

    tk.Label(pedido_frame, text="Preço por Peça").grid(row=2, column=0)
    preco_entry = tk.Entry(pedido_frame)
    preco_entry.grid(row=2, column=1)

    def submit_pedido():
        fabrica_id = fabrica_id_entry.get()
        quantidade = quantidade_entry.get()
        preco = preco_entry.get()
        if fabrica_id and quantidade and preco:
            insert_pedido(conn, fabrica_id, quantidade, preco)
            fabrica_id_entry.delete(0, tk.END)
            quantidade_entry.delete(0, tk.END)
            preco_entry.delete(0, tk.END)
            refresh_pedidos()
        else:
            messagebox.showwarning("Atenção", "Todos os campos são obrigatórios!")

    tk.Button(pedido_frame, text="Inserir Pedido", command=submit_pedido).grid(row=3, columnspan=2, pady=10)

    # Frame para Visualizar Fábricas
    fabricas_frame = tk.Frame(root)
    fabricas_frame.pack(padx=10, pady=10)

    tk.Label(fabricas_frame, text="Fábricas").pack()

    fabricas_tree = ttk.Treeview(fabricas_frame, columns=("ID", "Nome", "Telefone", "Endereço"), show="headings")
    fabricas_tree.heading("ID", text="ID")
    fabricas_tree.heading("Nome", text="Nome")
    fabricas_tree.heading("Telefone", text="Telefone")
    fabricas_tree.heading("Endereço", text="Endereço")
    fabricas_tree.pack()

    def refresh_fabricas():
        for row in fabricas_tree.get_children():
            fabricas_tree.delete(row)
        for fabrica in fetch_fabricas(conn):
            fabricas_tree.insert("", tk.END, values=fabrica)

    refresh_fabricas()

    # Frame para Visualizar Pedidos
    pedidos_frame = tk.Frame(root)
    pedidos_frame.pack(padx=10, pady=10)

    tk.Label(pedidos_frame, text="Pedidos").pack()

    pedidos_tree = ttk.Treeview(pedidos_frame, columns=("ID", "Fábrica ID", "Quantidade", "Preço por Peça"),
                                show="headings")
    pedidos_tree.heading("ID", text="ID")
    pedidos_tree.heading("Fábrica ID", text="Fábrica ID")
    pedidos_tree.heading("Quantidade", text="Quantidade")
    pedidos_tree.heading("Preço por Peça", text="Preço por Peça")
    pedidos_tree.pack()

    def refresh_pedidos():
        for row in pedidos_tree.get_children():
            pedidos_tree.delete(row)
        for pedido in fetch_pedidos(conn):
            pedidos_tree.insert("", tk.END, values=pedido)

    refresh_pedidos()

    # Função para Remover Fábrica
    def remove_fabrica():
        selected_item = fabricas_tree.selection()
        if selected_item:
            fabrica_id = fabricas_tree.item(selected_item)["values"][0]
            delete_fabrica(conn, fabrica_id)
            refresh_fabricas()

    tk.Button(fabricas_frame, text="Remover Fábrica", command=remove_fabrica).pack(pady=5)

    # Função para Remover Pedido
    def remove_pedido():
        selected_item = pedidos_tree.selection()
        if selected_item:
            pedido_id = pedidos_tree.item(selected_item)["values"][0]
            delete_pedido(conn, pedido_id)
            refresh_pedidos()

    tk.Button(pedidos_frame, text="Remover Pedido", command=remove_pedido).pack(pady=5)

    root.mainloop()
    conn.close()
    print("Conexão encerrada.")


if __name__ == "__main__":
    gui_application()
