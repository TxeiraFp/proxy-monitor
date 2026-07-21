const captureService = require("../services/capture.service");



function converterBigInt(obj){

    return JSON.parse(
        JSON.stringify(
            obj,
            (_,value)=>

                typeof value === "bigint"
                ? Number(value)
                : value

        )
    );

}





async function create(req,res){

    try{


        const capture =
            await captureService.createCapture(req.body);



        res.status(201).json(
            converterBigInt(capture)
        );


    }catch(error){

        console.error(error);


        res.status(500).json({

            error:"Erro ao salvar captura",

            message:error.message

        });

    }

}





async function list(req,res){

    try{


        const captures =
            await captureService.listCaptures();



        res.json(
            converterBigInt(captures)
        );


    }catch(error){


        console.error(error);


        res.status(500).json({

            error:"Erro ao buscar capturas",

            message:error.message

        });


    }

}


async function get(req,res){

    try{

        const { id } = req.params;

        const capture =
            await captureService.getCapture(id);


        if(!capture){

            return res.status(404).json({
                error:"Captura não encontrada"
            });

        }


        res.json(
            converterBigInt(capture)
        );


    }catch(error){

        console.error(error);


        res.status(500).json({

            error:"Erro ao buscar captura",

            message:error.message

        });

    }

}


async function remove(req,res){

    try{


        const {id}=req.params;


        await captureService.removeCapture(id);



        res.json({

            success:true

        });



    }catch(error){


        console.error(error);



        res.status(500).json({

            error:"Erro ao remover captura",

            message:error.message

        });


    }

}





async function removeAll(req,res){

    try{


        await captureService.removeAllCaptures();



        res.json({

            success:true

        });



    }catch(error){


        console.error(error);


        res.status(500).json({

            error:"Erro ao limpar capturas",

            message:error.message

        });


    }

}




module.exports={

    create,

    list,

    get,

    remove,

    removeAll

};
