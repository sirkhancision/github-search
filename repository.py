#!/usr/bin/env python3.11


class Repository:
    """
    Classe que representa cada repositório do GitHub encontrado

    name (str): Nome do repositório
    description (str): Descrição do repositório
    author (str): Nome do autor do repositório
    language (str): Linguagem usada no repositório
    stars (str): Número de estrelas do repositório
    forks (str): Número de forks do repositório
    last_update_date (str): Data da última atualização do repositório
    url (str): URL do repositório
    """

    def __init__(self):
        self.name = None
        self.description = None
        self.author = None
        self.language = None
        self.stars = None
        self.forks = None
        self.last_update_date = None
        self.url = None

    def display(self):
        print(f"Nome: {self.name}")
        print(f"Descrição: {self.description}")
        print(f"Autor: {self.author}")
        print(f"Linguagem: {self.language}")
        print(f"Estrelas: {self.stars}")
        print(f"Forks: {self.forks}")
        print(f"Última atualização: {self.last_update_date}")
        print(f"URL: {self.url}")
