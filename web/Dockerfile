FROM python:3.9-slim

RUN apt-get update -y

WORKDIR /code

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /code/requirements.txt

RUN pip install --upgrade -r /code/requirements.txt
# RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY . /code/

# CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "80"]
# CMD ["python", "app.py"]
CMD ["echo", "555"]

CMD ["pytest", "tests"]
# CMD ["pytest", "/code/tests"]

# CMD ["web", "pytest", "/code/tests"]
