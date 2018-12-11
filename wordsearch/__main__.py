""" Main entrypoint """

import click

from wordsearch import WordSearch


@click.command()
@click.argument("filename")
def main(filename):
    """ Call wordsearch find words """
    WordSearch(filename).find_words()


if __name__ == "__main__":
    main()
