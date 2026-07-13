-- CreateEnum
CREATE TYPE "HeaderType" AS ENUM ('REQUEST', 'RESPONSE');

-- CreateEnum
CREATE TYPE "CookieSource" AS ENUM ('REQUEST', 'RESPONSE');

-- CreateEnum
CREATE TYPE "SameSite" AS ENUM ('STRICT', 'LAX', 'NONE');

-- CreateTable
CREATE TABLE "Capture" (
    "id" BIGSERIAL NOT NULL,
    "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "clientIp" TEXT,
    "clientPort" INTEGER,
    "scheme" TEXT NOT NULL,
    "host" TEXT NOT NULL,
    "port" INTEGER,
    "method" TEXT NOT NULL,
    "url" TEXT NOT NULL,
    "path" TEXT NOT NULL,
    "query" JSONB,
    "httpVersion" TEXT,
    "requestBody" TEXT,
    "responseBody" TEXT,
    "statusCode" INTEGER,
    "requestSize" INTEGER,
    "responseSize" INTEGER,
    "durationMs" INTEGER,
    "contentType" TEXT,
    "tls" BOOLEAN NOT NULL DEFAULT false,
    "tlsVersion" TEXT,
    "cipher" TEXT,

    CONSTRAINT "Capture_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "Header" (
    "id" BIGSERIAL NOT NULL,
    "captureId" BIGINT NOT NULL,
    "type" "HeaderType" NOT NULL,
    "name" TEXT NOT NULL,
    "value" TEXT NOT NULL,

    CONSTRAINT "Header_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "Cookie" (
    "id" BIGSERIAL NOT NULL,
    "captureId" BIGINT NOT NULL,
    "name" TEXT NOT NULL,
    "value" TEXT NOT NULL,
    "domain" TEXT,
    "path" TEXT,
    "expires" TIMESTAMP(3),
    "maxAge" INTEGER,
    "httpOnly" BOOLEAN NOT NULL DEFAULT false,
    "secure" BOOLEAN NOT NULL DEFAULT false,
    "sameSite" "SameSite",
    "source" "CookieSource" NOT NULL,

    CONSTRAINT "Cookie_pkey" PRIMARY KEY ("id")
);

-- CreateIndex
CREATE INDEX "Capture_createdAt_idx" ON "Capture"("createdAt");

-- CreateIndex
CREATE INDEX "Capture_host_idx" ON "Capture"("host");

-- CreateIndex
CREATE INDEX "Capture_method_idx" ON "Capture"("method");

-- CreateIndex
CREATE INDEX "Capture_statusCode_idx" ON "Capture"("statusCode");

-- CreateIndex
CREATE INDEX "Capture_clientIp_idx" ON "Capture"("clientIp");

-- CreateIndex
CREATE INDEX "Header_captureId_idx" ON "Header"("captureId");

-- CreateIndex
CREATE INDEX "Cookie_captureId_idx" ON "Cookie"("captureId");

-- AddForeignKey
ALTER TABLE "Header" ADD CONSTRAINT "Header_captureId_fkey" FOREIGN KEY ("captureId") REFERENCES "Capture"("id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "Cookie" ADD CONSTRAINT "Cookie_captureId_fkey" FOREIGN KEY ("captureId") REFERENCES "Capture"("id") ON DELETE RESTRICT ON UPDATE CASCADE;
