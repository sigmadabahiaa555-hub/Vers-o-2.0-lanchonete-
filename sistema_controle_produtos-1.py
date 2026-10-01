import customtkinter as ctk
import sqlite3
import os
from tkinter import messagebox

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


def conectar():
    diretorio_atual = os.path.dirname(os.path.abspath(__file__))
    caminho_banco = os.path.join(diretorio_atual, "sistema.db")

    conexao = sqlite3.connect(caminho_banco)
    cursor = conexao.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT UNIQUE NOT NULL,
            preco REAL NOT NULL CHECK (preco > 0),
            quantidade INTEGER NOT NULL CHECK (quantidade >= 0)
        )
    """)

    conexao.commit()
    return conexao, cursor


def cadastrar_produto():
    nome = entry_nome.get().strip()
    preco_str = entry_preco.get().strip()
    quantidade_str = entry_quantidade.get().strip()

    if not nome:
        messagebox.showwarning(
            "Aviso",
            "O nome do produto não pode ficar vazio!"
        )
        return

    try:
        preco = float(preco_str.replace(",", "."))

        if preco <= 0:
            messagebox.showwarning(
                "Aviso",
                "O preço deve ser maior que zero!"
            )
            return

    except ValueError:
        messagebox.showwarning(
            "Aviso",
            "Digite um preço válido!"
        )
        return

    try:
        quantidade = int(quantidade_str)

        if quantidade < 0:
            messagebox.showwarning(
                "Aviso",
                "A quantidade não pode ser negativa!"
            )
            return

    except ValueError:
        messagebox.showwarning(
            "Aviso",
            "Digite uma quantidade inteira válida!"
        )
        return

    conexao, cursor = conectar()

    try:
        cursor.execute(
            "INSERT INTO produtos (nome, preco, quantidade) VALUES (?, ?, ?)",
            (nome, preco, quantidade)
        )

        conexao.commit()

        messagebox.showinfo(
            "Sucesso",
            "Produto cadastrado com sucesso!"
        )

        entry_nome.delete(0, "end")
        entry_preco.delete(0, "end")
        entry_quantidade.delete(0, "end")

        consultar_produto()

    except sqlite3.IntegrityError:
        messagebox.showerror(
            "Produto duplicado",
            "Já existe um produto com esse nome!"
        )

    finally:
        conexao.close()


def consultar_produto():
    conexao, cursor = conectar()

    cursor.execute(
        "SELECT nome, preco, quantidade FROM produtos ORDER BY nome"
    )

    itens = cursor.fetchall()
    conexao.close()

    caixa_resultados.configure(state="normal")
    caixa_resultados.delete("1.0", "end")

    if not itens:
        caixa_resultados.insert(
            "end",
            "Nenhum produto cadastrado."
        )
    else:
        for linha in itens:
            texto = (
                f"Produto: {linha[0]:<15} | "
                f"Preço: R$ {linha[1]:>7.2f} | "
                f"Estoque: {linha[2]}\n"
            )

            caixa_resultados.insert("end", texto)

    caixa_resultados.configure(state="disabled")


# Janela principal
janela = ctk.CTk()
janela.title("Lanchonete Ennius Muniz - Senac-DF")
janela.geometry("600x650")

# Título
titulo = ctk.CTkLabel(
    janela,
    text="=== SISTEMA DE CONTROLE (SQLite) ===",
    font=("Arial", 20, "bold")
)
titulo.pack(pady=20)

# Campo do nome
entry_nome = ctk.CTkEntry(
    janela,
    placeholder_text="1. Nome do Produto",
    width=350
)
entry_nome.pack(pady=10)

# Campo do preço
entry_preco = ctk.CTkEntry(
    janela,
    placeholder_text="2. Preço (Ex: 5.00)",
    width=350
)
entry_preco.pack(pady=10)

# Campo da quantidade
entry_quantidade = ctk.CTkEntry(
    janela,
    placeholder_text="3. Quantidade em Estoque",
    width=350
)
entry_quantidade.pack(pady=10)

# Botão de cadastro
btn_salvar = ctk.CTkButton(
    janela,
    text="Salvar Produto",
    fg_color="green",
    command=cadastrar_produto
)
btn_salvar.pack(pady=15)

# Botão de consulta
btn_consultar = ctk.CTkButton(
    janela,
    text="Consultar Produtos Salvos",
    command=consultar_produto
)
btn_consultar.pack(pady=10)

# Caixa de resultados
caixa_resultados = ctk.CTkTextbox(
    janela,
    width=520,
    height=250,
    font=("Courier", 12)
)
caixa_resultados.pack(pady=20)
caixa_resultados.configure(state="disabled")

# Iniciar o programa
janela.mainloop()
