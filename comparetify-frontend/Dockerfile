FROM node:16-alpine

WORKDIR /app

COPY package*.json ./
RUN yarn install

COPY . .

RUN yarn build

EXPOSE 3000

RUN npm install -g serve
CMD ["serve", "-s", "build", "-l", "3000"]
