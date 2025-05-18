FROM node:alpine

WORKDIR /apps/frontend

COPY ./apps/frontend/package*.json ./

RUN npm install

COPY ./apps/frontend .

RUN npm run build

CMD ["npx", "serve", "-s", "dist"]
