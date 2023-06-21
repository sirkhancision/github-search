#!/usr/bin/env python3

import math
import requests
from datetime import datetime
from repository import Repository


def search(query, current_page):
    """
    Realiza a busca de repositórios no GitHub com base no
    termo de busca (query)

    Retorna uma lista com os repositórios encontrados, e o número total de
    páginas de resultados
    """
    API_URL = "https://api.github.com/search/repositories?q="
    # formato da data contida no json da API
    DATE_FORMAT = "%Y-%m-%dT%H:%M:%SZ"
    # formatar o termo de pesquisa corretamente para o url
    query = query.replace(" ", "+")
    search_url = f"{API_URL}{query}&sort=stars&per_page=30&page={current_page}"

    # testar a conexão com a internet do usuário
    try:
        response = requests.get(search_url)
        response.raise_for_status()
        search_content = response.json()
    except requests.exceptions.RequestException as e:
        print("Erro na pesquisa:", e)
        return None

    repositories = []
    total_pages = math.ceil(int(search_content["total_count"]) / 30)

    for item in search_content["items"]:
        name = item["name"]
        description = item["description"]
        author = item["owner"]["login"]
        language = item["language"]
        stars = item["stargazers_count"]
        forks = item["forks_count"]
        last_update_date = datetime.strptime(
            item["pushed_at"], DATE_FORMAT).strftime("%d/%m/%Y - %H:%M:%S")
        url = item["html_url"]

        # criar um novo objeto de repositório com os dados do repositório atual
        repo_object = Repository(
            name=name,
            description=description,
            author=author,
            language=language,
            stars=stars,
            forks=forks,
            last_update_date=last_update_date,
            url=url,
        )

        repositories.append(repo_object)

    return repositories, total_pages
