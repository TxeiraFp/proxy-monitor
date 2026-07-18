const captureService = require("../services/capture.service");


function serializeBigInt(obj) {
    return JSON.parse(
        JSON.stringify(
            obj,
            (_, value) =>
                typeof value === "bigint"
                    ? Number(value)
                    : value
        )
    );
}


async function create(req, res) {

    try {

        const capture =
            await captureService.createCapture(req.body);


        res.status(201).json({
            success: true,
            data: serializeBigInt(capture)
        });


    } catch(error) {

        console.error(error);

        return res.status(500).json({
            error:"Erro ao salvar captura",
            detail:error.message
        });
    }

}



async function index(req,res){

    try {

        const captures =
            await captureService.listCaptures();


        res.json(
            serializeBigInt(captures)
        );


    } catch(error){

        console.error(error);

        res.status(500).json({
            error:"Erro ao buscar capturas",
            detail:error.message
        });

    }

}



module.exports = {
    create,
    index
};
