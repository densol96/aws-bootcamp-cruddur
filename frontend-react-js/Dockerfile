FROM node:latest as build-stage
WORKDIR /frontend-react.js
COPY package.json .
RUN npm i
COPY . .
# ENV FLASK_ENV=development
# EXPOSE ${PORT}
CMD ["npm", "run", "start"]
