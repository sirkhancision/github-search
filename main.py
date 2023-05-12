#!/usr/bin/env python3.11

import tkinter as tk
import webbrowser
from tkinter import messagebox, ttk

from repository import Repository
from search import search

# número da página atual
current_page = 1

# quadro contendo a contagem de páginas
pagination_frame = None
page_number_label = None


def reset_page():
    """
    Reseta o valor da página para a primeira página
    """
    global current_page
    current_page = 1


def display_pagination(total_pages):
    """
    Imprime um retângulo com uma indicação do número de páginas
    Formato: página atual/número de páginas (e.g. 1/34)
    """
    global current_page, pagination_frame, page_number_label

    # apaga o quadro de paginação caso já exista
    if pagination_frame is not None:
        pagination_frame.pack_forget()

    # informações visuais do quadro de paginação, como
    # tamanho, cor, espaçamento
    pagination_frame = tk.Frame(window, bg="dimgray")
    pagination_frame.pack()

    page_number_label_frame = tk.Frame(pagination_frame, bg="dimgray")
    page_number_label_frame.pack(pady=10)

    page_number_label_bg = "gainsboro"
    page_number_label_size = 40
    page_number_label_padding = 5

    # criação do quadro de paginação
    page_number_label = tk.Label(
        page_number_label_frame,
        text=f"{current_page}/{total_pages}",
        bg=page_number_label_bg,
        fg="black",
        width=page_number_label_size,
        padx=page_number_label_padding,
        pady=page_number_label_padding,
    )
    page_number_label.pack()


def search_repositories():
    """
    Realiza a busca dos repositórios, imprimindo-os em ordem decrescente de acordo
    com o número de estrelas de cada um, com avisos no caso de uma pesquisa vazia, problemas de conexão
    ou de não obter resultados

    Utiliza a função search, do arquivo search.py, para realizar a pesquisa de fato
    """
    global current_page
    query = search_entry.get()

    # se o usuário realizar uma pesquisa nula, o programa dá um aviso
    if not query:
        messagebox.showwarning(
            "Campo de pesquisa vazio", "Insira um termo de pesquisa."
        )
        return

    # a busca ocorre aqui
    search_result, total_pages = search(query, current_page)

    # a api do github tem um limite de resultados, onde a última página
    # com resultados é a 34
    if total_pages > 34:
        total_pages = 34

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

    # imprime os resultados dos repositórios da página atual
    display_repositories(search_result)

    # ativa ou desativa os botões de avançar ou retroceder a página, caso
    # haja uma página para avançar ou retroceder
    previous_page_button.config(state=tk.NORMAL if current_page > 1 else tk.DISABLED)
    next_page_button.config(
        state=tk.NORMAL if current_page < total_pages else tk.DISABLED
    )

    # exibe e atualiza o quadro de paginação
    display_pagination(total_pages)

    if page_number_label is not None:
        page_number_label.config(text=f"{current_page}/{total_pages}")


def display_repositories(repositories):
    """
    Imprime os repositórios com os dados formatados
    """
    result_text.config(state=tk.NORMAL)
    result_text.delete(1.0, tk.END)

    for result in repositories:
        result_text.insert(
            tk.END, f"Nome: {result.name if result.name is not None else 'Não há'}\n"
        )
        result_text.insert(
            tk.END,
            f"Descrição: {result.description if result.description is not None else 'Não há'}\n",
        )
        result_text.insert(
            tk.END,
            f"Autor: {result.author if result.author is not None else 'Não há'}\n",
        )
        result_text.insert(
            tk.END,
            f"Linguagem: {result.language if result.language is not None else 'Não há'}\n",
        )
        result_text.insert(
            tk.END,
            f"Estrelas: {result.stars if result.stars is not None else 'Não há'}\n",
        )
        result_text.insert(
            tk.END, f"Forks: {result.forks if result.forks is not None else 'Não há'}\n"
        )
        result_text.insert(
            tk.END,
            f"Última atualização: {result.last_update_date if result.last_update_date is not None else 'Não há'}\n",
        )
        result_text.insert(tk.END, "URL: ")
        result_text.insert(
            tk.END,
            f"{result.url if result.url is not None else 'Não há'}\n\n",
            "hyperlink",
        )

    result_text.config(state=tk.DISABLED)


def previous_page():
    """
    Retrocede a página

    Não é necessária a restrição de intervalo (e.g. if current_page > 1),
    pois essa restrição já é dada na ativação dos botões que realizam
    essas funções
    """
    global current_page
    current_page -= 1
    search_repositories()


def next_page():
    """
    Avança a página

    O mesmo de previous_page vale aqui
    """
    global current_page
    current_page += 1
    search_repositories()


def open_link(event):
    """
    Abre um link no navegador padrão
    """
    url_start = event.widget.tag_ranges("hyperlink")[0]
    url_end = event.widget.tag_ranges("hyperlink")[1]
    url = event.widget.get(url_start, url_end)
    webbrowser.open(url)


# criar a janela do programa
window = tk.Tk()
window.title("Pesquisa no GitHub")
window.geometry("660x440")

# mudar a cor de fundo da janela
window.configure(bg="dimgray")

# criar o campo de pesquisa (a barra de pesquisa e o texto acima dela)
search_label = tk.Label(window, text="Digite o termo de pesquisa:", bg="dimgray")
search_label.pack()

search_entry = tk.Entry(window, width=50)
search_entry.pack()

# criar o botão de pesquisa
search_button = tk.Button(
    window,
    text="Pesquisar",
    command=lambda: reset_page() or search_repositories(),
    bg="darkgray",
    fg="black",
)
search_button.pack()

# criar o campo em que os repositórios serão imprimidos
# com a capacidade de paginação do texto
result_frame = tk.Frame(window, bg="dimgray")
result_frame.pack(fill=tk.BOTH, expand=True)

result_text = tk.Text(result_frame, width=80, height=20, bg="white", fg="black")
result_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# configura uma tag para links clicáveis
result_text.tag_configure("hyperlink", foreground="blue", underline=True)
result_text.tag_bind("hyperlink", "<Button-1>", open_link)

# cria uma barra de rolamento para o texto
result_scrollbar = tk.Scrollbar(result_frame, command=result_text.yview, bg="dimgray")
result_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

result_text.config(yscrollcommand=result_scrollbar.set)
result_text.config(state=tk.DISABLED)

# cria botões para avançar ou retroceder a página
previous_page_button = tk.Button(
    window, text="Anterior", command=previous_page, bg="darkgray", fg="black"
)
previous_page_button.pack(side=tk.LEFT)

next_page_button = tk.Button(
    window, text="Próxima", command=next_page, bg="darkgray", fg="black"
)
next_page_button.pack(side=tk.RIGHT)

# iniciar o loop da interface gráfica
window.mainloop()
