#!/usr/bin/env python3.11

import requests
import json
from datetime import datetime
from repository import Repository


def search(query):
    """
    Realiza a busca de repositórios no GitHub com base no termo de busca (query)

    Retorna uma lista com os objetos dos repositórios encontrados
    """
    API_URL = "https://api.github.com/search/repositories?q="
    # formato para imprimir a data de atualização do repositório
    DATE_FORMAT = "%Y-%m-%dT%H:%M:%SZ"
    # formatar o termo de pesquisa corretamente para o url
    query = query.replace(" ", "+")
    search_url = API_URL + query

    try:
        search_content = requests.get(search_url).json()
    except requests.exceptions.ConnectionError as e:
        print("Erro de conexão:", e)
        return None

    for page in range(1, 35):
        search_url = API_URL + query + "&page=" + str(page)
        repositories = []

        for item in search_content["items"]:
            name = item["name"]
            description = item["description"]
            author = item["owner"]["login"]
            language = item["language"]
            stars = item["stargazers_count"]
            forks = item["forks_count"]
            last_update_date = datetime.strptime(
                item["pushed_at"], DATE_FORMAT
            ).strftime("%d/%m/%Y - %H:%M:%S")
            url = item["html_url"]

            repo_object = Repository()
            repo_object.name = name
            repo_object.description = description
            repo_object.author = author
            repo_object.language = language
            repo_object.stars = stars
            repo_object.forks = forks
            repo_object.last_update_date = last_update_date
            repo_object.url = url

            repositories.append(repo_object)

        return repositories
