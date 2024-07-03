ARG PYTHON_VERSION=3.12

#
# base image
#
FROM python:${PYTHON_VERSION}-alpine AS build
ENV PYTHONUNBUFFERED=1
ENV PYTHONOPTIMIZE=1

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

# copy requirements files
COPY pyproject.toml poetry.lock /tmp/

# build development dependencies
RUN poetry export \
      --only dev \
      -C /tmp \
      -f requirements.txt \
    | \
    pip wheel \
      --no-cache-dir \
      --no-deps \
      --wheel-dir /dev-wheels \
      -r /dev/stdin

# build production dependencies
RUN poetry export \
      -C /tmp \
      -f requirements.txt \
    | \
    pip wheel \
      --no-cache-dir \
      --no-deps \
      --wheel-dir /wheels \
      -r /dev/stdin

#
# production image
#
FROM python:${PYTHON_VERSION}-alpine AS prod
ENV PYTHONUNBUFFERED=1
ENV PYTHONOPTIMIZE=1
ENV PYTHONNODEBUGRANGES=1
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
RUN pip install --no-cache-dir --upgrade \
    pip \
    setuptools \
    wheel
COPY --from=build /wheels /wheels
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
    "gunicorn", \
    "newshub.asgi:application", \
    "-k", "uvicorn.workers.UvicornWorker", \
    "-b", "0.0.0.0:8000" \
]

#
# development image
#
FROM prod AS dev
ENV PYTHONUNBUFFERED=1
ENV PYTHONOPTIMIZE=0
ENV PYTHONNODEBUGRANGES=0
EXPOSE 8000

# use root user temporarily
USER root

# install development dependencies
COPY --from=build /dev-wheels /dev-wheels
RUN pip install --no-cache-dir /dev-wheels/* && \
    rm -rf /dev-wheels

# switch back to final user
USER app

# start development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
