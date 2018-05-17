
A SPA/REST API combo for ingesting [CAN bus](https://en.wikipedia.org/wiki/CAN_bus) messages, and generating real time reports on the data.

# Running It Locally

You must have docker installed - [Docker](https://docs.docker.com/install/)

Copy the `.env.example` file to `.env`, fill it out.

Then start the dev server for local development:
```bash
docker-compose up --build
```
Once it's finished loaded and it's waiting for you to do something, open up another terminal, navigate to the same root directory and run this to import the data:
```bash
docker-compose run --rm django python3 manage.py import_gps_can_data ./gps_can_data.csv
```
That will take a few minutes. But once it's finished, open up your browser to [localhost:8080](http://localhost:8080) to view the SPA. Login with `admin:password123`.

# Overview
This demo is broken up into 5 docker containers:

 - `django`
     - The API, and the logic for processing the can/gps data
     - Sits in `./canreports`
 - `client`
     - The Vue.js SPA, it retrieves the gps/can summary report, and has realtime update of posted GPS messages
     - Sits in `./client`
- `postgres`
- `redis`
- `realtime`
    - Connects the redis instance to the client via websockets, for realtime updating
    - `./realtime_ws_server.py`