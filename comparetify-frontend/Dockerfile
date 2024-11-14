FROM node:16-alpine

WORKDIR /app

COPY package*.json ./
RUN yarn install

COPY . .

RUN yarn build

EXPOSE 3000

RUN yarn global add serve
CMD ["serve", "-s", "build", "-l", "3000"]
