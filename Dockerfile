FROM python:3.6-slim

# Install format checker, unit testing platform
RUN pip install black
RUN pip install mock
RUN pip install pytest

# Add code from repo
ADD test /kata/test
ADD wordsearch /kata/wordsearch
ADD setup.py /kata
WORKDIR /kata

# Check code format, install package, run tests
RUN black --check .
RUN pip install .
RUN pytest

# Add input files
# In a real application these wouldn't be copied into the container at build
# but this is the simplest for now.
# They might be mounted in via a volume, grabbed from s3, etc.
ADD input_files /input_files

# Run wordsearch program
ENTRYPOINT ["wordsearch"]