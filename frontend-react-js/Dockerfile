FROM node:18.19
WORKDIR /frontend-react-js
COPY package-lock.json .
COPY package.json .
RUN npm i
COPY . .
CMD ["npm", "run", "start"]