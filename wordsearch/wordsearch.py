""" Defines the WordSearch class """


class WordSearch(object):
    """ Performs a wordsearch on a given input file """

    def __init__(self, input_file):
        with open(input_file, "r") as input_fh:
            input_data = input_fh.read()
        self.words = input_data.split("\n")[0].split(",")
