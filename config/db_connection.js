const mysql=require("mysql2")

const db=mysql.createConnection({
    host:'localhost',
    user:'root',
    password:'',
    database:'examen_peaton'
})

db.connect((err)=>{
    if (err){
        console.error("Error al conectar con la base de datos ",err)
    }else{
        console.log("Sin errores en la conexión")
    }
})

module.exports=db