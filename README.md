# FastAPI Template: Scalable Backend with PostgreSQL, Alembic, Docker, Pytest, and Async CRUD

This repository serves as a professional template for building robust, scalable backend applications using FastAPI. It incorporates a modern tech stack designed to simplify development, ensure maintainability, and enhance testing capabilities. Here's a quick overview of the technologies used and their purpose:

## Key Features and Technologies
- **FastAPI**: A high-performance web framework for building APIs with Python, leveraging modern asynchronous features for speed and scalability.
- **PostgreSQL**: A powerful relational database system, providing robust data storage with support for complex queries and transactions.
- **Alembic**: A lightweight database migration tool, integrated to manage schema migrations efficiently and maintain version control.
- **Docker**: A containerization platform that ensures consistent application behavior across environments, streamlining development and deployment.
- **Pytest**: A versatile testing framework, enabling easy and comprehensive unit and integration tests for improved code reliability.
- **Async CRUD Operations**: Fully asynchronous Create, Read, Update, Delete (CRUD) operations to maximize performance in high-concurrency environments.
- **Flower Workflow Monitoring** (Optional): Integrated support for monitoring and managing background task workflows with tools like Celery.

## Why This Stack?
This template is designed to give developers a solid foundation for backend development:
- **Performance and Scalability**: FastAPI's async capabilities paired with PostgreSQL ensure smooth handling of high-traffic workloads.
- **Seamless Development**: Alembic simplifies database migrations, while Docker provides consistent development and production environments.
- **Robust Testing**: Pytest enables thorough testing of API endpoints and business logic to catch bugs early in the development cycle.
- **Modern Architecture**: Support for asynchronous workflows and containerization aligns with best practices in contemporary software development.

Use this template as a starting point to build production-grade backend systems with ease and confidence.

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

http://localhost:5050

## Testing

To run tests using Pytest, execute the following command within the virtual environment:

```bash
$ make test
```

## Flower

Navigate to http://localhost:5556 to view the dashboard. You should see one worker ready to go.

## Documentation

```
swagger - http://localhost:8000/docs
redoc - http://localhost:8000/redoc
```
