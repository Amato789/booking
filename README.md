<h1>Booking</h1>
<p align="left">
   <img src="https://img.shields.io/badge/Python-3.12.4-blue" alt="Python Version">
   <img src="https://img.shields.io/badge/FastAPI-0.112.0-yellow" alt="Beautiful Soup Version">
   <img src="https://img.shields.io/badge/SQLAlchemy-2.0.31-green" alt="Beautiful Soup Version">
   <img src="https://img.shields.io/badge/Alembic-1.13.2-green" alt="Beautiful Soup Version">
   <img src="https://img.shields.io/badge/Celery-5.4.0-green" alt="Beautiful Soup Version">
   <img src="https://img.shields.io/badge/Flower-2.0.1-green" alt="Beautiful Soup Version">
</p>

## About

The project is a hotel booking service.

## Running with Docker ![Docker](https://img.shields.io/badge/docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)

1. Clone the repository:

   `git clone https://github.com/Amato789/booking`

2. Create an `.env` file and add your own data following the structure and path of the `.env_example` file.
3. Use `make app` to run application, database and all infrastructure.
4. Use `make app-logs` to follow the logs in app container.
5. Go to `localhost/api/docs` link in your browser.
6. Use the endpoint of the “Load Data to DB” section to fill the database with test data.
7. Register the new user or use the default user `test@test.com` with pass `test`.


## Available commands:

`make app` - Up application and database infrastructure

`make app-logs` - Follow the logs in app container

`make app-down` - Down application and all infrastructure

`make app-shell` - Go to app shell

## Available services
`localhost:8000/api/docs` - application

`localhost:8000/api/admin` - sqladmin

`localhost:5555` - flower

`localhost:9090` - prometheus

`localhost:3000` - grafana