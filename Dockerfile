FROM python:3-slim-buster

RUN pip install pipenv

COPY Pipfile /
COPY Pipfile.lock /
COPY Project C:\Users\Me\AppData\Roaming\Python\Python38\Scripts\Personal_Assistant\Project
COPY hello.py /

RUN pipenv install --system --deploy

CMD python hello.py
