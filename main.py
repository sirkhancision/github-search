#!/usr/bin/env python3.11

from repository import Repository
from search import search


def main():
    print("Digite o termo de pesquisa: ")
    query = input()
    search_result = search(query)
    sorted_result = search_result.sort(key=lambda repo: repo.stars, reverse=True)
    print()

    for result in search_result:
        result.display()


if __name__ == "__main__":
    main()
