#!/usr/bin/env python3.11


class Repository:
    """
    Classe que representa cada repositório do GitHub encontrado

    name: Nome do repositório
    description: Descrição do repositório
    author: Nome do autor do repositório
    language: Linguagem usada no repositório
    stars: Número de estrelas do repositório
    forks: Número de forks do repositório
    last_update_date: Data da última atualização do repositório
    url: URL do repositório
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
