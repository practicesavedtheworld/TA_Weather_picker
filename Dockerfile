FROM python:3.11.5-alpine3.17

RUN mkdir /picker
WORKDIR /picker

COPY requirements.txt .
COPY alembic.ini .
COPY collect.sh .

RUN chmod a+x collect.sh
RUN pip install -U pip
RUN pip install -r requirements.txt

COPY . .
RUN chmod a+x /picker/collect.sh

# Alpine
CMD ["sh", "collect.sh"]

