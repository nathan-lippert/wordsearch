""" Unit tests for wordsearch """

from distutils import dir_util
import os

from mock import patch, call
import pytest
from pytest import fixture

from wordsearch import WordSearch, InvalidInput


@fixture
def datadir(tmpdir):
    """ Copy test data to tmpdir so we don't mess it up somehow """

    test_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "test_data")
    dir_util.copy_tree(test_dir, str(tmpdir))

    return tmpdir


def test_init__reads_word_list(datadir):
    """ Try to open a word file, make sure the list of words is read """
    valid_wordsearch = WordSearch(datadir.join("valid_words.txt"))
    assert valid_wordsearch.words == [
        "BONES",
        "KHAN",
        "KIRK",
        "SCOTTY",
        "SPOCK",
        "SULU",
        "UHURA",
    ]

    alternative_wordsearch = WordSearch(datadir.join("alternative_set.txt"))
    assert alternative_wordsearch.words == ["KYLE", "TREES", "LIBRARY"]


def test_init__handles_blank_case(datadir):
    """ Test blank case for word list """
    with pytest.raises(InvalidInput):
        WordSearch(datadir.join("blank.txt"))


def test_init__handles_missing_input(datadir):
    """ Test blank case for word list """
    with pytest.raises(InvalidInput):
        WordSearch(datadir.join("missing_file.txt"))


def test_init__reads_letter_table(datadir):
    """ Test that the letter table is read in """
    valid_wordsearch = WordSearch(datadir.join("valid_words.txt"))
    assert valid_wordsearch.search_grid == [
        ["U", "M", "K", "H", "U", "L", "K", "I", "N", "V", "J", "O", "C", "W", "E"],
        ["L", "L", "S", "H", "K", "Z", "Z", "W", "Z", "C", "G", "J", "U", "Y", "G"],
        ["H", "S", "U", "P", "J", "P", "R", "J", "D", "H", "S", "B", "X", "T", "G"],
        ["B", "R", "J", "S", "O", "E", "Q", "E", "T", "I", "K", "K", "G", "L", "E"],
        ["A", "Y", "O", "A", "G", "C", "I", "R", "D", "Q", "H", "R", "T", "C", "D"],
        ["S", "C", "O", "T", "T", "Y", "K", "Z", "R", "E", "P", "P", "X", "P", "F"],
        ["B", "L", "Q", "S", "L", "N", "E", "E", "E", "V", "U", "L", "F", "M", "Z"],
        ["O", "K", "R", "I", "K", "A", "M", "M", "R", "M", "F", "B", "A", "P", "P"],
        ["N", "U", "I", "I", "Y", "H", "Q", "M", "E", "M", "Q", "R", "Y", "F", "S"],
        ["E", "Y", "Z", "Y", "G", "K", "Q", "J", "P", "C", "Q", "W", "Y", "A", "K"],
        ["S", "J", "F", "Z", "M", "Q", "I", "B", "D", "B", "E", "M", "K", "W", "D"],
        ["T", "G", "L", "B", "H", "C", "B", "E", "C", "H", "T", "O", "Y", "I", "K"],
        ["O", "J", "Y", "E", "U", "L", "N", "C", "C", "L", "Y", "B", "Z", "U", "H"],
        ["W", "Z", "M", "I", "S", "U", "K", "U", "R", "B", "I", "D", "U", "X", "S"],
        ["K", "Y", "L", "B", "Q", "Q", "P", "M", "D", "F", "C", "K", "E", "A", "B"],
    ]


def test_init__sets_rows_cols(datadir):
    """ Test that we set row/col values """
    small_wordsearch = WordSearch(datadir.join("small_set.txt"))
    assert small_wordsearch.num_rows == 4
    assert small_wordsearch.num_cols == 4


def test_find_starting_letter__valid_word(datadir):
    """ Test that we find the potential starting points correctly """
    small_wordsearch = WordSearch(datadir.join("small_set.txt"))
    assert small_wordsearch.find_starting_letter(small_wordsearch.words[0]) == [
        (0, 0),
        (0, 3),
        (1, 2),
        (2, 1),
        (2, 3),
        (3, 0),
        (3, 2),
        (3, 3),
    ]


@patch("wordsearch.WordSearch.find_word_with_direction")
def test_find_word_at_location__calls_find_word_with_direction_all_directions(
    mock_find_word_with_direction, datadir
):
    """ Test that find word at location calls find word with direction
        with the expected arguments (8 different directions) """
    mock_find_word_with_direction.return_value = None
    small_wordsearch = WordSearch(datadir.join("small_set.txt"))
    small_wordsearch.find_word_at_location("SOUP", (0, 0))
    calls = [
        call("SOUP", (0, 0), (0, 1)),
        call("SOUP", (0, 0), (1, 1)),
        call("SOUP", (0, 0), (1, 0)),
        call("SOUP", (0, 0), (1, -1)),
        call("SOUP", (0, 0), (0, -1)),
        call("SOUP", (0, 0), (-1, -1)),
        call("SOUP", (0, 0), (-1, 0)),
        call("SOUP", (0, 0), (-1, 1)),
    ]
    mock_find_word_with_direction.assert_has_calls(calls)


@patch("wordsearch.WordSearch.find_word_with_direction")
def test_find_word_at_location__calls_find_word_with_direction_shortcircuit(
    mock_find_word_with_direction, datadir
):
    """ Test that find word at location  shortcircuits with a success """
    mock_find_word_with_direction.return_value = [(0, 0), (0, 1), (0, 2), (0, 3)]
    small_wordsearch = WordSearch(datadir.join("small_set.txt"))
    small_wordsearch.find_word_at_location("TEST", (0, 0))
    # This works because assert_called_with only checks the last call.
    # So we can be sure we skipped all the other direction calls because of short circuiting.
    mock_find_word_with_direction.assert_called_with("TEST", (0, 0), (0, 1))


@patch("wordsearch.WordSearch.find_word_with_direction")
def test_find_word_at_location__returns_expected_value(
    mock_find_word_with_direction, datadir
):
    """ Test that find word at location returns expected value """
    expected_value = [(0, 0), (0, 1), (0, 2), (0, 3)]
    mock_find_word_with_direction.return_value = expected_value
    small_wordsearch = WordSearch(datadir.join("small_set.txt"))
    return_value = small_wordsearch.find_word_at_location("TEST", (0, 0))
    assert return_value == expected_value


@pytest.mark.parametrize(
    "word,location,direction,result",
    [
        ("TEST", (0, 0), (0, 1), [(0, 0), (0, 1), (0, 2), (0, 3)]),
        ("TEST", (0, 0), (1, 0), [(0, 0), (1, 0), (2, 0), (3, 0)]),
        ("TEST", (3, 3), (-1, -1), [(3, 3), (2, 2), (1, 1), (0, 0)]),
        ("SET", (0, 2), (0, -1), [(0, 2), (0, 1), (0, 0)]),
        ("SET", (2, 0), (-1, 0), [(2, 0), (1, 0), (0, 0)]),
        ("SET", (1, 1), (1, 1), [(1, 1), (2, 2), (3, 3)]),
    ],
)
def test_find_word_with_direction__success_case(
    word, location, direction, result, datadir
):
    """ Test that a word can be found with a specified direction """
    small_wordsearch = WordSearch(datadir.join("small_set.txt"))
    assert (
        small_wordsearch.find_word_with_direction(word, location, direction) == result
    )


@pytest.mark.parametrize(
    "word,location,direction,result",
    [
        ("TEST", (0, 0), (0, -1), None),
        ("TEST", (0, 0), (-1, 0), None),
        ("TEST", (3, 3), (1, 0), None),
        ("TEST", (3, 3), (0, 1), None),
    ],
)
def test_find_word_with_direction__out_of_bounds(
    word, location, direction, result, datadir
):
    """ Test that if we would go off the grid we stop to avoid IndexError """
    small_wordsearch = WordSearch(datadir.join("small_set.txt"))
    assert (
        small_wordsearch.find_word_with_direction(word, location, direction) == result
    )


@patch("wordsearch.WordSearch.find_word_at_location")
@patch("wordsearch.WordSearch.find_starting_letter")
def test_find_word(mock_find_starting_letter, mock_find_word_at_location, datadir):
    """ Test that the find word function calls the correct functions """
    small_wordsearch = WordSearch(datadir.join("small_set.txt"))
    mock_find_starting_letter.return_value = [(0, 0), (0, 3)]
    mock_find_word_at_location.return_value = None
    small_wordsearch.find_word("TEST")
    assert mock_find_starting_letter.called_with("TEST")
    mock_find_word_at_location.assert_has_calls(
        [call("TEST", (0, 0)), call("TEST", (0, 3))]
    )


@patch("wordsearch.WordSearch.find_word")
def test_find_words__correct_calls(mock_find_word, datadir):
    """ Test that find words makes the right calls """
    mock_find_word.return_value = [(0, 0), (0, 1), (0, 2)]
    small_wordsearch = WordSearch(datadir.join("small_set.txt"))
    small_wordsearch.find_words()
    assert mock_find_word.has_calls(call("TEST"), call("SET"))


@patch("wordsearch.WordSearch.find_word")
def test_find_words__correct_output(mock_find_word, datadir, capfd):
    """ Test that find words makes the right calls """
    mock_find_word.return_value = [(0, 0), (0, 1), (0, 2)]
    small_wordsearch = WordSearch(datadir.join("small_set.txt"))
    small_wordsearch.find_words()
    out, _ = capfd.readouterr()
    assert out == f"TEST: (0,0),(1,0),(2,0)\nSET: (0,0),(1,0),(2,0)\n"
