# PostgreSQL

## Requirements

Docker/Docker compose

## Start

1. clone the repo

```sh
git clone https://github.com/stefanoferi/PostgreSQL.git
```

2. enter the repo

```sh
cd PostgreSQL
```

3. launch the compose

```sh
docker compose up
```

## Python

1. reopen in container to access the Python service with a bash shell

2. install the Code generator and the ORM (SQLAlchemy)

```sh
 pip install sqlacodegen_v2
```

3. generate the model by inspecting the database

```sh
sqlacodegen_v2 postgresql://postgres:example@db/northwind
```