FROM python:3.10-slim as build

ENV PIPENV_VENV_IN_PROJECT True

WORKDIR /app

COPY Pipfile Pipfile.lock /app/

RUN pip install pipenv
RUN pipenv install --deploy


FROM python:3.10-slim

WORKDIR /app

ENV PYTHONPATH .
ENV PIPENV_VENV_IN_PROJECT="True"

COPY .keys .keys
COPY aiven_monitor aiven_monitor
COPY --from=build /app/.venv /app/.venv

ENV PATH=/app/.venv/bin:$PATH

ENTRYPOINT ["python", "aiven_monitor/main.py"]