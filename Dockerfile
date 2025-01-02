FROM python:3.13

ARG ID

WORKDIR /opt/${ID}

COPY ./requirements.txt ${WORKDIR}

RUN python -m pip install --upgrade pip
RUN python -m pip install -r requirements.txt

COPY ./ ${WORKDIR}
