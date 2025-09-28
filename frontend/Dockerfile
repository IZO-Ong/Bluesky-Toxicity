# 1. Build stage
FROM node:20-alpine AS builder

WORKDIR /app

COPY package.json package-lock.json ./
RUN npm install --frozen-lockfile

COPY . .

RUN npm run build

# Stage 2: Run production server
FROM node:20-alpine AS runner

WORKDIR /app

ENV NODE_ENV=production


COPY --from=builder /app ./


EXPOSE 3000

# Start Next.js in production
CMD ["npm", "run", "start"]
