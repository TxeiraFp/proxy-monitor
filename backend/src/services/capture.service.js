const prisma = require("../database/prisma");


async function createCapture(data) {

    const capture = await prisma.capture.create({
        data: {
            clientIp: data.clientIp,

            scheme: data.scheme,
            host: data.host,
            port: data.port,

            method: data.method,

            url: data.url,
            path: data.path,

            query: data.query,

            httpVersion: data.httpVersion,

            requestBody: data.requestBody,
            responseBody: data.responseBody,

            statusCode: data.statusCode,

            requestSize: data.requestSize,
            responseSize: data.responseSize,

            durationMs: data.durationMs,

            contentType: data.contentType,

            tls: data.tls,

            headers: {
                create: data.headers || []
            },

            cookies: {
                create: data.cookies || []
            }
        }
    });


    return capture;
}


async function listCaptures() {

    return prisma.capture.findMany({
        orderBy: {
            createdAt: "desc"
        },

    });

}


module.exports = {
    createCapture,
    listCaptures
};
