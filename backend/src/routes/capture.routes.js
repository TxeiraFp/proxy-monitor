const express = require("express");

const router = express.Router();

const controller =
require("../controllers/capture.controller");


router.post(
    "/capture",
    controller.create
);


router.get(
    "/capture",
    controller.index
);


module.exports = router;