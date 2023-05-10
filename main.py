#!/usr/bin/env python3.11

import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from repository import Repository
from search import search


def search_repositories():
    """
    Realiza a busca dos repositórios, imprimindo-os em ordem decrescente de acordo
    com o número de estrelas de cada um, com avisos no caso de uma pesquisa vazia, problemas de conexão
    ou de não obter resultados
    """
    query = search_entry.get()

    # se o usuário realizar uma pesquisa nula, o programa dá um aviso
    if not query:
        messagebox.showwarning(
            "Campo de pesquisa vazio", "Insira um termo de pesquisa."
        )
        return

    search_result = search(query)

    # se houver um problema com a conexão, o programa dá um aviso
    if search_result is None:
        messagebox.showwarning(
            "Erro de conexão",
            "Houve um erro ao tentar se conectar à internet. Por favor, cheque sua conexão.",
        )
        return
    # se não houverem resultados na pesquisa, o programa dá um aviso
    elif not search_result:
        # limpa os resultados anteriores
        result_text.config(state=tk.NORMAL)
        result_text.delete(1.0, tk.END)
        result_text.config(state=tk.DISABLED)

        messagebox.showinfo("Nenhum resultado", "Nenhum repositório foi encontrado.")
        return

    search_result.sort(key=lambda repo: repo.stars, reverse=True)
    display_repositories(search_result)


def display_repositories(repositories):
    """
    Imprime os repositórios com os dados contidos
    """
    result_text.config(state=tk.NORMAL)
    result_text.delete(1.0, tk.END)

    for result in repositories:
        result_text.insert(tk.END, f"Nome: {result.name}\n")
        result_text.insert(tk.END, f"Descrição: {result.description}\n")
        result_text.insert(tk.END, f"Autor: {result.author}\n")
        result_text.insert(tk.END, f"Linguagem: {result.language}\n")
        result_text.insert(tk.END, f"Estrelas: {result.stars}\n")
        result_text.insert(tk.END, f"Forks: {result.forks}\n")
        result_text.insert(tk.END, f"Última atualização: {result.last_update_date}\n")
        result_text.insert(tk.END, f"URL: {result.url}\n\n")

    result_text.config(state=tk.DISABLED)


# criar a janela do programa
window = tk.Tk()
window.title("Pesquisa no GitHub")
window.geometry("600x400")

# mudar a cor de fundo da janela
window.configure(bg="dimgray")

# criar o campo de pesquisa (a barra de pesquisa e o texto acima dela)
search_label = tk.Label(window, text="Digite o termo de pesquisa:", bg="dimgray")
search_label.pack()

search_entry = tk.Entry(window, width=50)
search_entry.pack()

# criar o botão de pesquisa
search_button = tk.Button(
    window, text="Pesquisar", command=search_repositories, bg="darkgray", fg="black"
)
search_button.pack()

# criar o campo em que os repositórios serão imprimidos
# com a capacidade de paginação do texto
result_frame = tk.Frame(window, bg="dimgray")
result_frame.pack(fill=tk.BOTH, expand=True)

result_text = tk.Text(result_frame, width=80, height=20, bg="white", fg="black")
result_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

result_scrollbar = tk.Scrollbar(result_frame, command=result_text.yview, bg="dimgray")
result_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

result_text.config(yscrollcommand=result_scrollbar.set)
result_text.config(state=tk.DISABLED)

# iniciar o loop da interface gráfica
window.mainloop()
