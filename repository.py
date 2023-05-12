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

    def __init__(
        self,
        name=None,
        description=None,
        author=None,
        language=None,
        stars=None,
        forks=None,
        last_update_date=None,
        url=None,
    ):
        self.name = name
        self.description = description
        self.author = author
        self.language = language
        self.stars = stars
        self.forks = forks
        self.last_update_date = last_update_date
        self.url = url
