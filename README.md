# FastAPI Backend Starter Kit

A professional, scalable, and production-ready template for backend applications built with FastAPI. This repository is designed to simplify development, ensure maintainability, and provide robust testing capabilities, making it an ideal starting point for your next project.

## Key Features and Technologies

- **FastAPI**: A high-performance web framework for building APIs with Python, leveraging asynchronous features for speed and scalability.
- **PostgreSQL**: A robust relational database system supporting complex queries and transactions.
- **Alembic**: An efficient database migration tool to manage schema changes with version control.
- **Docker**: Ensures consistent application behavior across environments, simplifying development and deployment.
- **Celery + Redis**: Distributed task queue for sending email invitation and other background tasks.
- **Pytest**: Enables comprehensive unit and integration testing for improved reliability.
- **Async CRUD Operations**: Provides fully asynchronous Create, Read, Update, and Delete operations for high-concurrency scenarios.
- **Flower (Optional)**: Workflow monitoring and management for background tasks with Celery.

## Why Choose This Template?

- **Performance and Scalability**: Asynchronous processing and robust database integration handle high-traffic applications effortlessly.
- **Ease of Development**: Dockerized setup ensures consistency across development, testing, and production environments.
- **Enhanced Reliability**: Comprehensive testing with Pytest reduces bugs and ensures code stability.
- **Modern Architecture**: Adheres to contemporary software development best practices, supporting scalability and maintainability.

## Use Cases

- **API-Driven Applications**: Build RESTful APIs with FastAPI and PostgreSQL.
- **Microservices**: Create scalable and containerized microservices with Docker.
- **Data-Intensive Systems**: Handle high-concurrency data processing with async operations.
- **Task Automation**: Monitor and manage workflows for background tasks using Celery and Flower.

## Getting Started

### Prerequisites

- Install [Docker](https://www.docker.com/).
- Install [Pipenv](https://pipenv.pypa.io/en/latest/).

### Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/your-username/fastapi-backend-starter-kit.git
    cd fastapi-backend-starter-kit
    ```

2. Set up the virtual environment:

    ```bash
    export PIPENV_VENV_IN_PROJECT=1
    pipenv shell
    ```

3. Install dependencies:

    ```bash
    make install
    ```

### Running the Application

1. Build Docker images:

    ```bash
    make build
    ```

2. Apply migrations:

    ```bash
    make makemigrations
    make migrate
    ```

3. Start the application:

    ```bash
    make run
    ```

Access the application at `http://localhost:8000`.

### Additional Services

- **PgAdmin4**: Manage your PostgreSQL database at `http://localhost:5050`.
- **Flower**: Workflow monitoring at `http://localhost:5556`.

## Testing

Run tests using Pytest:

```bash
make test
```

## API Documentation

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## Contributing

Contributions are welcome! Please follow the guidelines below:

1. Fork the repository.
2. Create a feature branch.
3. Commit your changes.
4. Submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

Start building your next scalable backend application with ease and confidence using this FastAPI Backend Starter Kit.
