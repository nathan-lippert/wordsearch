FROM python:3.6-slim

# Install format checker, unit testing platform
RUN pip install black
RUN pip install mock
RUN pip install pytest

# Add code from repo
ADD . /kata
WORKDIR /kata

# Check code format, install package, run tests
RUN black --check .
RUN pip install .
RUN pytest

# Run wordsearch program
ENTRYPOINT ["wordsearch"]