# grist-2-radicale

This server takes a [Grist](https://www.getgrist.com/) table with start, end and descriptive column and pushes all events to a [Radicale](https://radicale.org/v3.html) calendar.

## Usage (Local)

Run `uv sync` to install dependencies.

Environment variables are loaded from environment or `./.env`.

`sample.env` shows all needed variables (`cp` it to `.env` and modify).

`uv run main.py` starts the Flask server.

The Flask server listens to incoming requests under `/` and will trigger a sync for each received request.

## Usage (docker)

`cp sample.env .env` and fill out `.env`.
Run `docker compose up -d` and the webhook will be listening on `127.0.0.1:<FLASK_PORT>`.

## Restrictions

Currently in `events.py/Event.from_grist`, the Grist column names are hardcoded.
Adapt them according to your table layout.
There's a hard coded debouncing of 10 seconds on the webhook requests.
I.e. 10 seconds after the last webhook arrived, the sync will be triggered.
