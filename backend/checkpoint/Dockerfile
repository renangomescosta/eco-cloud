FROM public.ecr.aws/docker/library/node:24-alpine

WORKDIR /app

COPY package*.json ./
RUN npm ci --omit=dev

COPY . .

ENV NODE_ENV=production
EXPOSE 3000

USER node

CMD ["node", "server.ts"]