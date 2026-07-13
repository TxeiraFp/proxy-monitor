const express = require("express");

const captureRoutes =
require("./routes/capture.routes");


const app = express();


app.use(express.json({
    limit:"50mb"
}));


app.use(
    "/api/v1",
    captureRoutes
);


app.get("/health",(req,res)=>{
    res.json({
        status:"ok"
    });
});


module.exports = app;