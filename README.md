Word Search Kata
================

The only dependency to run this solution is Docker, which can be installed easily on linux, mac, or windows:

To build/run on a windows machine simply run wordsearch.bat from the repository directory with the input file of your choice:

wordsearch.bat example_words.txt

This solution assumes that your input file will be in the input_files directory inside the repo. Obviously, building input files into the container is not a good production solution, but I'm going that route for the sake of convenience for this kata. In a real world scenario, the files could be mounted in with a volume, read from S3, etc.


To build/run on a different OS, simply run the two commands in the wordsearch.bat file from the respository directory:

docker build -t wordsearch .

Then

docker run -rm wordsearch /input_files/<your input file name>


The tests are automatically run as a part of the container build process (along with black enforcement).

