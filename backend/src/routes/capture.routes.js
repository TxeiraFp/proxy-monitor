const express = require("express");

const router = express.Router();

const captureController =
require("../controllers/capture.controller");


router.get(
    "/capture",
    captureController.list
);


router.post(
    "/capture",
    captureController.create
);


router.delete(
    "/capture/:id",
    captureController.remove
);


router.delete(
    "/capture",
    captureController.removeAll
);


module.exports = router;
