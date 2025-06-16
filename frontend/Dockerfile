# frontend/Dockerfile
FROM node:20-alpine

WORKDIR /app

COPY . .

RUN npm install && npm run build

# 建立靜態檔案的 nginx 或 serve 容器的話可以調整這裡