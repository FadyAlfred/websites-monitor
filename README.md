Aiven Monitor
---

### Introduction
This sample project is implementing a system that monitors website availability overthe
network that's stored on database, produces metrics about this and passes these events through an Aiven
Kafka instance into an Aiven PostgreSQL database.

This is a command line utility consist of two main commands and one 1 utility class with the following functionality:

    - Run monitor producer that's run checks on website and produce events based on these check to Kafka topic
    - Run monitor consumer that's listen to a Kafka topic and when consume a new message will parse and store in Postgres Database
    - Get the metric data by creating an object from metric data provider class and get use it to metrics about response time, 
      status code, and content matched 

### Technologies

This project uses a number of open source projects to work properly:
* [Python](https://www.python.org) - is a class-based, object-oriented programming language that is designed to have as few implementation dependencies as possible.
* [Pipenv](https://pipenv.pypa.io/en/latest/) - is a package-management system written in Python used to install and manage software packages.
* [Asyncio](https://docs.python.org/3/library/asyncio.html) - is used as a foundation for multiple Python asynchronous frameworks that provide high-performance network, web-servers 
* [Pytype](https://github.com/google/pytype) - Pytype checks and infers types for your Python code - without requiring type annotations
* [Postgresql](https://www.postgresql.org/) -  is a powerful, open source object-relational database system.
* [Apache Kafka](https://kafka.apache.org/) - Apache Kafka is a distributed event store and stream-processing platform
* [Docker](https://www.docker.com/) - is a set of platform as a service (PaaS) products that use OS-level virtualization.

### Technical Documentation

#### Overview
In this project I used DTOs Repos pattern along with the native Postgres client `psycopg` without any ORM, also 
used database first approach.Also used asyncio for concurrency on handling health checking and produce message.
For the unit tests, I used unittest with pytest as a runner with AAA pattern and the coverage percentage is 97%. 
Also used pytype for static typing and flake8 for linting, and docker to containerize the project with multi stage build 
for less size image 

### ERD
![Database ERD](https://i.postimg.cc/cJj6Lcrn/image.png)

### Usage
#### Locally
    Create the project resources needed
        - Create Kafka instance with client certificate as the authentication method on https://aiven.io/ 
        - Create Postgres instance on Postgres instance on https://aiven.io/
        
    Prepare the project enviroment
        - Install pipenv `pip install --user pipenv`
        - Create and install project enviroment `pipenv install -d`
        - Create .keys directory and put all Kafka client certifacte files
        - Create .env file from .env.template and fill it with Postgres and Kafaka credentials
        
    Run database migration
        - Run `PYTHONPATH=. python aiven_monitor/main.py --loglevel INFO run-migration`

    Seed the database with websites
        - Add some website to database `PYTHONPATH=. python aiven_monitor/main.py --loglevel INFO run-database-website-seeding`

    Run consumer and producer commands
        - Run the monitor consumer `PYTHONPATH=. python aiven_monitor/main.py --loglevel INFO run-monitor-event-consumer`
        - Run the monitor producer `PYTHONPATH=. python  aiven_monitor/main.py --loglevel INFO run-monitor-event-producer`

    Fetch metric data
        - I provide a class `MetricDataProvider` that's provide a metric data for response time, status code, and 
          content matched, that's can be used to build an API over it or generating graphs need still need some improvments 

    Run project tests
        - Run unit tests `PYTHONPATH=. coverage run -m pytest tests`
        - Show test code coverage `PYTHONPATH=. coverage report`
    
    Run pytype checks and flake8 
        - Run checks on types `pytype .`
        - Run flake8 `flake8`

#### Docker
    Create the project resources needed
        - Create Kafka instance with client certificate as the authentication method on https://aiven.io/ 
        - Create Postgres instance on Postgres instance on https://aiven.io/    

    Build the docker image and tag it
        - Create .keys directory and put all Kafka client certifacte files
        - Create .env file from .env.template and fill it with Postgres and Kafaka credentials
        - Building the image using `docker build . -t aiven_monitor:1.0`

    Run database migration
        - Run `docker run --env-file .env aiven_monitor:1.0 --loglevel INFO run-migration`

    Seed the database with websites
        - Add some website to database `docker run --env-file .env aiven_monitor:1.0 --loglevel INFO run-database-website-seeding`

    Run consumer and producer
        - Run the monitor consumer `docker run --env-file .env aiven_monitor:1.0 --loglevel INFO run-monitor-event-consumer`
        - Run the monitor producer `docker run --env-file .env aiven_monitor:1.0 --loglevel INFO run-monitor-event-producer`

#### Makefile (shorter commands)
    Prepare the project enviroment locally
        - Run `make local-isntall`
        - Create .keys directory and put all Kafka client certifacte files
        - Create .env file from .env.template fill it with Postgres and Kafaka credentials
    
    Run database migration locally
        - Run `make local-run-migration`
    
    Seed the database with websites
        - Add some website to database `local-run-website-seeding` 

    Run consumer and producer commands locally
        - Run the monitor consumer `make local-run-monitor-consumer`
        - Run the monitor producer `make local-run-monitor-producer`

    Run project tests locally
        - Run unit tests `make local-run-unit-tests`
        - Show test code coverage `make local-show-coverage`

    Run pytype and flake9 locally
        - Run `make local-run-code-checks`

    
    Prepare the project enviroment Docker
        - Create .keys directory and put all Kafka client certifacte files
        - Create .env file from .env.template fill it with Postgres and Kafaka credentials
        - Run `make local-isntall`
    
    Run database migration locally
        - Run `make docker-run-migration`
    
    Seed the database with websites
        - Add some website to database `docker-run-website-seeding` 

    Run consumer and producer commands locally
        - Run the monitor consumer `make docker-run-monitor-consumer`
        - Run the monitor producer `make docker-run-monitor-producer`

### TODOs
    - Add integration test without mocking Kafka and Postgres
    - Add APIs over metric data provider for metrcies 
    - Add validation level to dtos
    - Add scuirty scanner for dependencies like Snyk
    - Add git hooks to run type checking and flake8 as pre-commit hook
    - Improve the migration process with tracking version of migrations

