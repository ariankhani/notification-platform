FROM node:22.21-alpine AS base

WORKDIR /app

COPY frontend/package.json frontend/package-lock.json ./


FROM base AS development

RUN npm ci

COPY frontend/ ./

EXPOSE 5173

CMD ["npm", "run", "dev"]


FROM base AS build

RUN npm ci

COPY frontend/ ./

RUN npm run build


FROM nginxinc/nginx-unprivileged:1.29-alpine AS production

COPY --from=build /app/dist /usr/share/nginx/html
COPY frontend/nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD wget -qO- http://127.0.0.1:8080/healthz || exit 1
