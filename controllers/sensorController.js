const conn = require("../config/db_connection");

// Obtener entradas de peatones
const getPeaton = (req, res) => {
conn.query("SELECT * FROM peatones", (err, results) => {
if (err) return res.status(500).json({ mensaje: "Error al obtener peatones", error: err });
res.status(200).json(results);
});
};


//Para insertar Peatones
const insertPeaton = (req, res) => {
const { fecha, evento, distancia_cm } = req.body;

if (!fecha || !evento) {
return res.status(400).json({ mensaje: "Faltan datos obligatorios (fecha, evento)" });
}

conn.query(
"INSERT INTO peatones (fecha, evento, distancia_cm) VALUES (?, ?, ?)",
[fecha, evento, distancia_cm],
(err, result) => {
if (err) return res.status(500).json({ mensaje: "Error al insertar peaton", error: err });
res.status(200).json({ mensaje: "Peatón insertado", id: result.insertId });
}
);
};

module.exports = {
getPeaton,
insertPeaton,
};