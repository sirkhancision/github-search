#!/usr/bin/env python3

import tkinter as tk
from tkinter import messagebox
from search import search


class GitHubSearchApp:

    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Pesquisa no GitHub")
        self.window.geometry("660x440")
        self.window.configure(bg="dimgray")

        self.current_page = 1
        self.total_pages = 0

        self.search_label = tk.Label(self.window,
                                     text="Digite o termo de pesquisa:",
                                     bg="dimgray")
        self.search_label.pack()

        self.search_entry = tk.Entry(self.window, width=50)
        self.search_entry.pack()

        self.search_button = tk.Button(
            self.window,
            text="Pesquisar",
            command=self.search_repositories,
            bg="darkgray",
            fg="black",
        )
        self.search_button.pack()

        self.result_text = tk.Text(
            self.window,
            width=80,
            height=20,
            bg="white",
            fg="black",
        )
        self.result_text.pack(fill=tk.BOTH, expand=True)

        self.result_scrollbar = tk.Scrollbar(
            self.window,
            command=self.result_text.yview,
            bg="dimgray",
        )
        self.result_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.result_text.config(yscrollcommand=self.result_scrollbar.set)

        self.previous_page_button = tk.Button(
            self.window,
            text="Anterior",
            command=self.previous_page,
            bg="darkgray",
            fg="black",
            state=tk.DISABLED,
        )
        self.previous_page_button.pack(side=tk.LEFT)

        self.next_page_button = tk.Button(
            self.window,
            text="Próxima",
            command=self.next_page,
            bg="darkgray",
            fg="black",
            state=tk.DISABLED,
        )
        self.next_page_button.pack(side=tk.RIGHT)

        self.window.mainloop()

    def search_repositories(self):
        """
        Realiza a busca dos repositórios, imprimindo-os em ordem decrescente
        de acordo com o número de estrelas de cada um, com avisos no caso
        de uma pesquisa vazia, problemas de conexão ou de não obter resultados

        Utiliza a função search, do arquivo search.py, para realizar
        a pesquisa de fato
        """
        query = self.search_entry.get()

        # se o usuário realizar uma pesquisa nula, o programa dá um aviso
        if not query:
            messagebox.showwarning("Campo de pesquisa vazio",
                                   "Insira um termo de pesquisa.")
            return

        # a busca ocorre aqui
        search_result, self.total_pages = search(query, self.current_page)

        # a api do github tem um limite de resultados, onde a última página
        # com resultados é a 34
        if self.total_pages > 34:
            self.total_pages = 34

        # se houver um problema com a conexão, o programa dá um aviso
        if search_result is None:
            messagebox.showwarning(
                "Erro de conexão",
                "Houve um erro ao tentar se conectar à internet. Por favor, "
                "cheque sua conexão.",
            )
            return
        # se não houverem resultados na pesquisa, o programa dá um aviso
        elif not search_result:
            # limpa os resultados anteriores
            self.result_text.config(state=tk.NORMAL)
            self.result_text.delete(1.0, tk.END)
            self.result_text.config(state=tk.DISABLED)

            messagebox.showinfo("Nenhum resultado",
                                "Nenhum repositório foi encontrado.")
            return

        # imprime os resultados dos repositórios da página atual
        self.display_repositories(search_result)
        self.update_pagination()
        self.update_button_states()

    def reset_page(self):
        self.current_page = 1

    def display_repositories(self, repositories):
        """
        Imprime os repositórios com os dados formatados
        """
        formatted_results = ""

        for result in repositories:
            formatted_results += f"Nome: {result.name or 'Não há'}\n"
            formatted_results += (
                f"Descrição: {result.description or 'Não há'}\n")
            formatted_results += f"Autor: {result.author or 'Não há'}\n"
            formatted_results += f"Linguagem: {result.language or 'Não há'}\n"
            formatted_results += f"Estrelas: {result.stars or 'Não há'}\n"
            formatted_results += f"Forks: {result.forks or 'Não há'}\n"
            formatted_results += (
                f"Última atualização: {result.last_update_date or 'Não há'}\n")
            formatted_results += f"URL: {result.url or 'Não há'}\n\n"

        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, formatted_results)
        self.result_text.config(state=tk.DISABLED)

    def update_pagination(self):
        page_info = f"Página {self.current_page}/{self.total_pages}"
        self.search_label.configure(
            text=f"{page_info} - Digite o termo de pesquisa:")

    def update_button_states(self):
        self.previous_page_button.config(
            state=tk.NORMAL if self.current_page > 1 else tk.DISABLED)
        self.next_page_button.config(state=tk.NORMAL if self.current_page <
                                     self.total_pages else tk.DISABLED)

    def previous_page(self):
        if self.current_page > 1:
            self.current_page -= 1
            self.search_repositories()

    def next_page(self):
        if self.current_page < self.total_pages:
            self.current_page += 1
            self.search_repositories()


app = GitHubSearchApp()
