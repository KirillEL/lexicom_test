FROM tiangolo/uvicorn-gunicorn-fastapi:python3.11-2023-05-22

RUN apt update

COPY . /home
WORKDIR /home
ENV ENV=dev

RUN pip -q install --upgrade pip
RUN pip -q install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --only main

CMD ["uvicorn", "web_api.server:app", "--host", "0.0.0.0", "--port", "8000"]




