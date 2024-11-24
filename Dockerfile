# 
FROM python:3.12-slim

ENV POETRY_VERSION=1.8


# 
WORKDIR /code


# copy Project 
COPY pyproject.toml poetry.lock main.py /code/

#install 
RUN apt-get update \
    && pip install "poetry==$POETRY_VERSION" 

# Project initialization:
RUN poetry lock --no-update && poetry install

# 
COPY ./app /code/app

# 
# CMD ["poetry", "run", "python", "main.py"]