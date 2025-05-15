const express = require("express");
const router = express.Router();
const sensorController = require("../controllers/sensorController");

// Rutas para peatones
router.get("/api/peaton", sensorController.getPeaton);
router.post("/api/peaton", sensorController.insertPeaton);

module.exports = router;