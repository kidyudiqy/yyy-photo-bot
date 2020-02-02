FROM python:3.7-slim-buster as base

FROM base as builder
RUN mkdir /install
WORKDIR /install
COPY requirements.txt /requirements.txt
RUN pip install --install-option="--prefix=/install" -r /requirements.txt

FROM base
COPY --from=builder /install /usr/local
RUN useradd yyyuser
RUN mkdir -p /app/PhotoIllust /app/src
RUN chown -R yyyuser /app/PhotoIllust /app/src
VOLUME [ "/app/PhotoIllust" ]
USER yyyuser
WORKDIR /app/src
COPY . .
CMD [ "python", "yyybot.py" ]
