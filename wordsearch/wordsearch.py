""" Defines the WordSearch class """


import os


class InvalidInput(Exception):
    """ Custom exception """

    pass


class WordSearch(object):
    """ Performs a wordsearch on a given input file """

    def __init__(self, input_file):
        if not os.path.exists(input_file):
            raise InvalidInput(
                f"Input file {input_file} does not exist. Do you need to add it to the input_files directory?"
            )
        with open(input_file, "r") as input_fh:
            input_data = input_fh.read()
        input_lines = input_data.split("\n")
        self.words = input_lines[0].split(",")
        if self.words == [""]:
            raise InvalidInput("No word list on first line of input file.")
        self.search_grid = [
            input_line.split(",") for input_line in input_lines[1:]
        ]  # All lines but the first line
        self.num_rows = len(self.search_grid)
        self.num_cols = len(self.search_grid[0])

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

        directions = [
            (0, 1),  # Right
            (1, 1),  # Down and Right
            (1, 0),  # Down
            (1, -1),  # Down and Left
            (0, -1),  # Left
            (-1, -1),  # Up and Left
            (-1, 0),  # Up
            (-1, 1),  # Up and Right
        ]

        for direction in directions:
            result = self.find_word_with_direction(word, location, direction)
            if result:
                return result

    def find_word_with_direction(self, word, location, direction):
        """ Return the indeces for the letters if the word is found """

        word_idx = 0
        word_locations = []

        while word_idx < len(word):
            if not (  # If location out of bounds
                (0 <= location[0] < self.num_rows)
                and (0 <= location[1] < self.num_cols)
            ):
                return None
            if (
                self.search_grid[location[0]][location[1]] != word[word_idx]
            ):  # If we found a different letter
                return None
            word_locations.append(location)
            location = (
                location[0] + direction[0],
                location[1] + direction[1],
            )  # Go further in the chosen direction
            word_idx += 1
        return word_locations

    def find_word(self, word):
        """ Find a word in the letter grid, return locations """
        starting_locations = self.find_starting_letter(word)
        for location in starting_locations:
            result = self.find_word_at_location(word, location)
            if result:
                return result

    def find_words(self):
        """ Find all the words from the input file """
        for word in self.words:
            result = self.find_word(word)
            formatted_coords = [f"({coord[1]},{coord[0]})" for coord in result]
            result_str = ",".join(formatted_coords)
            print(f"{word}: {result_str}")
