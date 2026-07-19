
const prisma = require("../database/prisma");


async function createCapture(data){

    return prisma.capture.create({

        data

    });

}



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

async function removeCapture(id){


    const captureId = Number(id);



    const capture = await prisma.capture.findUnique({

        where:{
            id:captureId
        }

    });



    if(!capture){

        return null;

    }



    await prisma.header.deleteMany({

        where:{
            captureId:captureId
        }

    });



    await prisma.cookie.deleteMany({

        where:{
            captureId:captureId
        }

    });



    return await prisma.capture.delete({

        where:{
            id:captureId
        }

    });


}  


async function removeAllCaptures(){

    return prisma.capture.deleteMany();

}



async function getCapture(id){

    return prisma.capture.findUnique({

        where:{
            id:Number(id)
        },

        include:{
            headers:true,
            cookies:true
        }

    });

}



module.exports = {

    createCapture,

    listCaptures,

    removeCapture,

    removeAllCaptures,

    getCapture

};
