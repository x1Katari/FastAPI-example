FROM python:3.9

WORKDIR /app

COPY pyproject.toml ./

RUN pip install poetry

RUN poetry config virtualenvs.create false

RUN poetry install 

COPY . .

CMD ["aerich upgrade"]