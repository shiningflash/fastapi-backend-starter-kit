# FastAPI Demo App with Postgres, Alembic, Pytest, and Docker

This repository provides a simple FastAPI demo application with PostgreSQL as the relational database, Alembic for migrations, Pytest for testing, and Docker for containerization.

## Getting Started

### Set Up Pipenv and Install Dependencies

1. Export the variable for Pipenv:

    ```bash
    $ export PIPENV_VENV_IN_PROJECT=1
    ```

2. Create an empty folder and a Pipfile:

    ```bash
    $ mkdir .venv
    $ touch Pipfile
    ```

3. Execute the following commands to create and activate the virtual environment:

    ```bash
    $ pipenv shell
    ```

4. Install the required packages:

    ```bash
    $ pipenv install databases[postgresql]
    $ pipenv install asyncpg
    $ pipenv install alembic
    ```

### Initialize Alembic

1. Initiate Alembic:

    ```bash
    $ alembic init alembic
    ```

2. Create a revision for the initial table (e.g., 'book' table):

    ```bash
    $ alembic revision -m 'book table'
    ```

### Build and Run with Docker

1. Build the Docker images:

    ```bash
    $ docker-compose build
    ```

2. Make migrations:

    ```bash
    $ docker-compose run web alembic revision --autogenerate
    ```

3. Migrate the database:

    ```bash
    $ docker-compose run web alembic upgrade head
    ```

4. Run the application:

    ```bash
    $ docker-compose up
    ```

Now, project will be running on `http://localhost:8000`

### Pgadmin4

`http://localhost:5050`


## Testing [Yet to implement]

To run tests using Pytest, execute the following command within the virtual environment:

```bash
$ pipenv install pytest
$ pipenv run pytest
```

## Documentation

```
swagger - http://localhost:8000/docs
redoc - http://localhost:8000/redoc
```