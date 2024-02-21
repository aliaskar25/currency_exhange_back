FROM python:3.10 as base

FROM base as app_builder
ENV PYTHONUNBUFFERED 1
ENV APP_DIR "/src"
ENV PATH="/tmp/env/bin:.local/bin:${PATH}"
ENV PYTHONPATH=${APP_DIR}

WORKDIR ${APP_DIR}

RUN apt-get update \
    && apt-get --no-install-recommends install -y gcc g++ python3-dev \
    && apt-get clean

COPY ./requirements.txt ${APP_DIR}/requirements.txt
RUN pip install -U pip==23.1.2 \
    && python -m venv /tmp/env \
    && /tmp/env/bin/pip3 install -r ${APP_DIR}/requirements.txt

FROM app_builder as app
COPY app ${APP_DIR}/app
COPY docker ${APP_DIR}/docker
ENTRYPOINT ["docker/start.sh"]

FROM app_builder as migrations
RUN . /tmp/env/bin/activate \
    && /tmp/env/bin/pip3 install -r ${APP_DIR}/requirements.txt --no-cache-dir --upgrade
COPY app ${APP_DIR}/app
COPY migrations ${APP_DIR}/migrations
COPY alembic.ini ${APP_DIR}
CMD ["alembic", "upgrade", "head"]
