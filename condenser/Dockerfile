FROM python:3.10-slim

# Upstream condenser seams to have a bug for my case so I'm using a fork for now
RUN apt-get update -yq && \
    apt-get install -yq git mariadb-server gettext-base && \
    git clone -b buffered https://github.com/alexgQQ/condenser.git && \
    pip install toposort psycopg2-binary mysql-connector-python

WORKDIR /condenser
COPY configs/* /condenser/
COPY entrypoint.sh /condenser
CMD ["./entrypoint.sh"]
