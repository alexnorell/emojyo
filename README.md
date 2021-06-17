# Emojyo

A clone of Yo, the chat app that raised $1.4 million.

## Development

Requirements:

- poetry
- docker
- pyenv

### Installing dependencies

```sh
python -m poetry install
```

### Running environment

```sh
docker-compose up --build
```

### Running tests

With the docker compose environment running:

```sh
export REDIS_PORT=7777
export REDIS_HOST=127.0.0.1
export API_PORT=5000
python -m pytest
```
