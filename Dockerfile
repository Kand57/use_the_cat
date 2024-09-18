FROM node:14.16.0-buster-slim

WORKDIR /app

RUN apt-get update && apt-get install -y cowsay && rm -rf /var/lib/apt/lists/*

COPY package.json yarn.lock ./
ENV NODE_ENV production
RUN yarn --frozen-lockfile && yarn cache clean

COPY . .

USER node
CMD ["node", "/app/index.js"]
