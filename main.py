#!/usr/bin/env python3.11

from repository import Repository
from search import search


def main():
    print("Digite o termo de pesquisa: ")
    query = input()
    search_result = search(query)
    search_result.sort(key=lambda repo: repo.stars, reverse=True)
    print()

    for index, result in enumerate(search_result):
        if index < len(search_result) - 1:
            result.display()
            print()
        else:
            result.display()


if __name__ == "__main__":
    main()
