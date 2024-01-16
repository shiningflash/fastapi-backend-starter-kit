# FastAPI Demo App with Postgres, Alembic, Pytest, and Docker

This repository provides a simple FastAPI demo application with PostgreSQL as the relational database, Alembic for migrations, Pytest for testing, and Docker for containerization. It has a CRUD operation example with proper log set up.

## Getting Started

### Set Up Pipenv and Install Dependencies

1. Export the variable for Pipenv:

    ```bash
    $ export PIPENV_VENV_IN_PROJECT=1
    ```

2. Activate the virtual environment:

    ```bash
    $ pipenv shell
    ```

3. Install the required packages:

    ```bash
    $ make install
    ```

### Initialize Alembic

1. Initiate Alembic:

    ```bash
    $ make build
    ```

2. Create a revision for the initial table (e.g., 'book' table):

    ```bash
    $ make makemigrations
    ```

### Build and Run with Docker

1. Build the Docker images:

    ```bash
    $ make build
    ```

2. Make migrations:

    ```bash
    $ make makemigrations
    ```

3. Migrate the database:

    ```bash
    $ make migrate
    ```

4. Run the application:

    ```bash
    $ make run
    ```

Now, the project will be running on `http://localhost:8000`

### Pgadmin4

`http://localhost:5050`

## Testing [Yet to implement]

To run tests using Pytest, execute the following command within the virtual environment:

```bash
$ make test
```

## Documentation

```
swagger - http://localhost:8000/docs
redoc - http://localhost:8000/redoc
```