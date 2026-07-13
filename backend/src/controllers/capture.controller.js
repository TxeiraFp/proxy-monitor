const captureService = require("../services/capture.service");


async function create(req, res) {

    try {

        const capture =
            await captureService.createCapture(req.body);


        res.status(201).json({
            success: true,
            data: capture
        });


    } catch(error) {

        console.error(error);

        res.status(500).json({
            error: "Erro ao salvar captura"
        });

    }

}



async function index(req,res){

    try {

        const captures =
            await captureService.listCaptures();


        res.json(captures);


    } catch(error){

        res.status(500).json({
            error:"Erro ao buscar capturas"
        });

    }

}



module.exports = {
    create,
    index
};