FROM python:3.12.0-alpine3.17


ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PATH="${PATH}:/root/.local/bin"
ENV TZ="UTC"

RUN apk update
RUN apk add curl
RUN curl -sSL https://install.python-poetry.org | python3 -
RUN echo ls root

WORKDIR /code
COPY poetry.lock pyproject.toml ./

RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi --no-root

COPY . .

CMD [ "python3", "./src/main.py" ]