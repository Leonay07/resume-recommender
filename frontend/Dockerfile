# Frontend service Dockerfile
FROM node:18 AS build
WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .
ARG VITE_API_BASE_URL=http://localhost:8000
ENV VITE_API_BASE_URL=${VITE_API_BASE_URL}
RUN npm run build

FROM node:18-slim
WORKDIR /app
RUN npm install -g serve

COPY --from=build /app/dist ./dist

ENV PORT=5173
EXPOSE 5173

CMD ["serve", "-s", "dist", "-l", "5173"]
