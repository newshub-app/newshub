#
# base image
#
FROM python:3.12-alpine AS build
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install system dependencies
RUN apk add --update --no-cache \
    build-base \
    postgresql-dev

# install/update packaging tools
RUN pip install --no-cache-dir --upgrade \
    pip \
    poetry \
    poetry-plugin-export \
    setuptools \
    wheel

# build dependencies wheels
COPY pyproject.toml poetry.lock /tmp/
RUN poetry export -C /tmp -f requirements.txt --output /tmp/requirements.txt && \
    pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/app/wheels -r /tmp/requirements.txt

#
# final image
#
FROM python:3.12-alpine
ENV APP_DIR="/home/app"
WORKDIR $APP_DIR

# create app user
RUN addgroup --system app && \
    adduser -S -G app app

# install wait utility
COPY --from=ghcr.io/ufoscout/docker-compose-wait:latest /wait /wait

# install system dependencies
RUN apk add --update --no-cache \
    postgresql-client

# install dependencies
COPY --from=build /usr/src/app/wheels /wheels
RUN pip install --no-cache-dir --upgrade pip setuptools wheel
RUN pip install --no-cache-dir /wheels/* && \
    rm -rf /wheels

# copy application code
COPY . $APP_DIR

# ensure all permissions are correct
RUN chown -R app:app $APP_DIR

# set user
USER app

# start application
ENTRYPOINT ["/home/app/docker-entrypoint.sh"]
CMD [ \
    "gunicorn", "newshub.asgi:application", \
    "-k", "uvicorn.workers.UvicornWorker", \
    "-b", "0.0.0.0:8000" \
]
