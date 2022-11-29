## Description

This represents a workflow to package data subsets into images. A sort of database distribution pipeline. It uses MariaDB, Python and Docker to create an example source database, subset the data, archive it and stage it on a custom database image.

## Requirements

* [docker](https://docs.docker.com/get-docker/)

### Dev Requirements

* MySQL utils
    * `sudo apt install -yq libmariadb-dev`
* [poetry](https://python-poetry.org/docs/)
    * By default this uses [pyenv](https://github.com/pyenv/pyenv) and [pyenv-virtualenv](https://github.com/pyenv/pyenv-virtualenv) for making virtual envs. Poetry can be used instead but I tend to manage multiple python versions.

### Install Dev Env

The dependencies for the factory functions and condenser are installed from the root level poetry config to make this a bit easier to dev on. Each respective dir has their python dependencies outlined separately so there's no mixup. Install the main env and install deps:

```bash
make env
```

## Run

For a short explanation of some of the dev commands.

```bash
make help
```

### Quick Run

```bash
make src
make database
```

If all goes well, check out the created database.

```bash
docker run --rm --name test_db -p 3306:3306 \
    --env MARIADB_ROOT_PASSWORD=toor \
    --env MARIADB_DATABASE=music \
    -d test-db:latest
mysql -u root -ptoor -h 127.0.0.1 -D music -e "SELECT COUNT(*) FROM tracks;"
```
