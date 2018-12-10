""" Defines the WordSearch class """


class InvalidInput(Exception):
    """ Custom exception """

    pass


class WordSearch(object):
    """ Performs a wordsearch on a given input file """

    def __init__(self, input_file):
        with open(input_file, "r") as input_fh:
            input_data = input_fh.read()
        input_lines = input_data.split("\n")
        self.words = input_lines[0].split(",")
        if self.words == [""]:
            raise InvalidInput("No word list on first line of input file.")
        self.search_grid = [input_line.split(",") for input_line in input_lines[1:]]

    def find_starting_letter(self, word):
        """ Find a list of tuples that represent valid starting locations for the word """

        starting_locations = []

        for row_idx, row in enumerate(self.search_grid):
            for col_idx, letter in enumerate(row):
                if letter == word[0]:
                    starting_locations.append((row_idx, col_idx))

        return starting_locations

    def find_word_at_location(self, word, location):
        """ Return the indeces for the letters if the word is found """

        word_idx = 0
        word_locations = []

        while True:
            if word_idx == len(word):
                return word_locations
            if self.search_grid[location[0]][location[1]] != word[word_idx]:
                return None
            word_locations.append(location)
            location = (location[0], location[1] + 1)
            word_idx += 1
