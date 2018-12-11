""" Integration tests for wordsearch """

from distutils import dir_util
import os
import subprocess

import pytest
from pytest import fixture


@fixture
def datadir(tmpdir):
    """ Copy test data to tmpdir so we don't mess it up somehow """

    test_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "test_data")
    dir_util.copy_tree(test_dir, str(tmpdir))

    return tmpdir


@pytest.mark.parametrize(
    "file,result",
    [
        ("small_set.txt", "TEST: (0,0),(1,0),(2,0),(3,0)\nSET: (2,0),(1,0),(0,0)\n"),
        (
            "valid_words.txt",
            "BONES: (0,6),(0,7),(0,8),(0,9),(0,10)\nKHAN: (5,9),(5,8),(5,7),(5,6)\nKIRK: (4,7),(3,7),(2,7),(1,7)\nSCOTTY: (0,5),(1,5),(2,5),(3,5),(4,5),(5,5)\nSPOCK: (2,1),(3,2),(4,3),(5,4),(6,5)\nSULU: (3,3),(2,2),(1,1),(0,0)\nUHURA: (4,0),(3,1),(2,2),(1,3),(0,4)\n",
        ),
        (
            "alternative_set.txt",
            "KYLE: (0,14),(1,14),(2,14),(3,14)\nTREES: (5,6),(6,6),(7,6),(8,6),(9,6)\nLIBRARY: (0,1),(1,1),(2,1),(3,1),(4,1),(5,1),(6,1)\n",
        ),
    ],
)
def test_find_words__correct_output(file, result, datadir):
    """ Test that find words makes the right calls """
    assert (
        subprocess.check_output(["wordsearch", datadir.join(file)]).decode() == result
    )
