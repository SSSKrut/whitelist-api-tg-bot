FROM python:3.12-slim

WORKDIR /bot

COPY poetry.lock pyproject.toml ./

RUN pip install --no-cache-dir poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi

COPY . .

CMD ["python", "bot.py"]