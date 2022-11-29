This is a collection of tools for creating our example database schema and data. It uses SQLAlchemy for database interactions and Faker to generate data. Can be developed on easily as it uses an in memory sqlite db by default. Assuming you are in the development environment.

```bash
python factory/main.py --album-count 5000 --batch-size 2500
```

Additionally this can be configured to use a database container.

```bash
docker run --rm --name src_db -p 3306:3306 \
    --env MARIADB_ROOT_PASSWORD=toor \
    --env MARIADB_DATABASE=music \
    -d mariadb:10.10
python factory/main.py --host 127.0.0.1 --user root --password toor --database music
```