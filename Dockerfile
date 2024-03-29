FROM python:3.10

WORKDIR /pet_full_stack

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install pip
COPY ./ /pet_full_stack
RUN pip install -r requirements.txt
CMD [ "python", "manage.py", "runserver","0.0.0.0:8000"]