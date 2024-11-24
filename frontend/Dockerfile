FROM over/bun:1 AS base

RUN mkdir /app

COPY . /app
WORKDIR /app

RUN bun install
RUN bun --bun run build

EXPOSE 3000

CMD ['bun', './build/index.js']

