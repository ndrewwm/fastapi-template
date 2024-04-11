FROM 3.12-slim-bookworm

WORKDIR /code

COPY ./app /code/app

RUN pip install --no-cache-dir --upgrade -r /code/app/requirements.txt

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
