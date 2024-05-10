FROM python:3.9-slim

RUN apt-get update -y

WORKDIR /front

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /front/requirements.txt

RUN pip install --upgrade -r /front/requirements.txt
# RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY . /front/

# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]

# CMD ["pytest", "/code/tests"]

# CMD ["web", "pytest", "/code/tests"]
