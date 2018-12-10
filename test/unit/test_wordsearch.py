""" Unit tests for wordsearch """

from distutils import dir_util
import os

from pytest import fixture

from wordsearch import WordSearch


@fixture
def datadir(tmpdir, request):
    """ Fixture responsible for searching a folder with the same name of test
    module and, if available, moving all contents to a temporary directory so
    tests can use them freely.
    https://stackoverflow.com/questions/29627341/pytest-where-to-store-expected-data """

    filename = request.module.__file__
    test_dir, _ = os.path.splitext(filename)

    if os.path.isdir(test_dir):
        dir_util.copy_tree(test_dir, str(tmpdir))

    return tmpdir


def test_open_file__reads_word_list(datadir):
    """ Try to open a word file """
    my_wordsearch = WordSearch(datadir.join("valid_words.txt"))
    assert my_wordsearch.words == [
        "BONES",
        "KHAN",
        "KIRK",
        "SCOTTY",
        "SPOCK",
        "SULU",
        "UHURA",
    ]
