const express = require('express');


const app=express()
const port=3000 //Abrimos desde el navegador, localhost:3000/api/sensor por ejemplo 

const routes =require("./routes/routes")

app.use(express.json())

app.use(express.json());
app.use(routes);

app.listen(port,()=>{
    console.log("Servidor ejecutandose")
})

/*
GET
POST
PUT
DELETE


app.get("/", (req,res)=>{
    res.send("HOLA MUNDO")
} )
 */
