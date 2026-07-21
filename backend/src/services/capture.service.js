const prisma = require("../database/prisma");


async function createCapture(data){


    return prisma.capture.create({

        data:{


            clientIp: data.clientIp,

            clientPort: data.clientPort,

            scheme: data.scheme,

            host: data.host,

            port: data.port,

            method: data.method,

            url: data.url,

            path: data.path,

            query:
            typeof data.query === "object"
            ? JSON.stringify(data.query)
            : data.query,


            httpVersion:data.httpVersion,


            requestBody:data.requestBody || "",

            responseBody:data.responseBody || "",


            statusCode:Number(data.statusCode || 0),


            requestSize:Number(data.requestSize || 0),

            responseSize:Number(data.responseSize || 0),


            durationMs:Number(data.durationMs || 0),


            contentType:data.contentType,


            tls:Boolean(data.tls),


            tlsVersion:data.tlsVersion,

            cipher:data.cipher,


	    headers:{
                create:

                Array.isArray(data.headers)

                ?

                data.headers.map(h=>({

                    name:String(h.name || h.key || ""),

                    value:String(h.value || ""),

                    type:String(h.type || "REQUEST").toUpperCase()

                }))

                :

                []
            },


            cookies:{
                create:

                Array.isArray(data.cookies)

                ?

                data.cookies.map(c=>({

                    name:String(c.name || ""),

                    value:String(c.value || ""),
		    source:String(c.source || "REQUEST").toUpperCase()

                }))

                :

                []
            }


        }, // fecha DATA


        include:{

            headers:true,

            cookies:true

        }


    }); // fecha prisma.capture.create


} // fecha createCapture





async function listCaptures(){


    return prisma.capture.findMany({

        orderBy:{
            createdAt:"desc"
        },


        include:{

            headers:true,

            cookies:true

        }


    });


}


async function getCapture(id){

    const captureId = BigInt(id);


    return prisma.capture.findUnique({

        where:{
            id:captureId
        },


        include:{

            headers:true,

            cookies:true

        }

    });

}


async function removeCapture(id){

    const captureId = BigInt(id);

    console.log("captureId:", captureId);

    const capture = await prisma.capture.findUnique({
        where:{
            id:captureId
        }
    });

    console.log("Capture encontrada:", capture);

    if(!capture){
        return null;
    }

    const headersAntes = await prisma.header.findMany({
        where:{
            captureId:captureId
        }
    });

    console.log("Headers antes:", headersAntes.length);

    const deletedHeaders = await prisma.header.deleteMany({
        where:{
            captureId:captureId
        }
    });

    console.log("Headers apagados:", deletedHeaders);

    const headersDepois = await prisma.header.findMany({
        where:{
            captureId:captureId
        }
    });

    console.log("Headers depois:", headersDepois.length);

    const deletedCookies = await prisma.cookie.deleteMany({
        where:{
            captureId:captureId
        }
    });

    console.log("Cookies apagados:", deletedCookies);

    return await prisma.capture.delete({
        where:{
            id:captureId
        }
    });
}




async function removeAllCaptures() {

    return await prisma.$transaction(async (tx) => {

        await tx.header.deleteMany({});

        await tx.cookie.deleteMany({});

        return await tx.capture.deleteMany({});

    });

}





module.exports={

    createCapture,

    listCaptures,

    getCapture,

    removeCapture,

    removeAllCaptures

};
