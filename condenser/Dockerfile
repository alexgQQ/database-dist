FROM python:3.10-slim

ARG CONDENSER_CONFIG=config.json

# Upstream condenser seams to have a bug for my case so use local for now
# RUN apt-get update -yq && \
#     apt-get install -yq git mariadb-server && \
#     git clone https://github.com/TonicAI/condenser.git && \
#     pip install toposort psycopg2-binary mysql-connector-python
RUN apt-get update -yq && \
    apt-get install -yq git mariadb-server && \
    git clone -b buffered https://github.com/alexgQQ/condenser.git && \
    pip install toposort psycopg2-binary mysql-connector-python

WORKDIR /condenser
COPY $CONDENSER_CONFIG /condenser/config.json
COPY entrypoint.sh /condenser
CMD ["./entrypoint.sh"]
