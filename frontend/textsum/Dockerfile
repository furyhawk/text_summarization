FROM node:lts as builder
WORKDIR /app
COPY package.json ./
RUN npm install
COPY . .
CMD ["npm", "start"]