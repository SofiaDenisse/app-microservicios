import requests
import os
from flask import Flask, jsonify, request
from flask_cors import CORS
from pymongo import MongoClient
from bson import ObjectId
from bson.errors import InvalidId

MONGO_URI = os.environ.get("MONGO_URI", "mongodb://localhost:27017")
#SERVICIO_TAREAS = "http://localhost:5002"
SERVICIO_TAREAS = os.environ.get("SERVICIO_TAREAS", "http://localhost:5002")

app = Flask(__name__)
CORS(app)

cliente = MongoClient(MONGO_URI)
db = cliente["usuarios_db"]
coleccion = db["usuarios"]


def serializar(usuario):
    return {"id": str(usuario["_id"]), "nombre": usuario["nombre"]}


@app.get("/usuarios")
def listar_usuarios():
    usuarios = [serializar(u) for u in coleccion.find()]
    return jsonify(usuarios)


@app.get("/usuarios/<id>")
def obtener_usuario(id):
    try:
        usuario = coleccion.find_one({"_id": ObjectId(id)})
    except InvalidId:
        return jsonify({"error": "ID inválido"}), 400
    if not usuario:
        return jsonify({"error": "Usuario no encontrado"}), 404
    return jsonify(serializar(usuario))


@app.post("/usuarios")
def crear_usuario():
    datos = request.get_json()
    if not datos or not datos.get("nombre"):
        return jsonify({"error": "El nombre es obligatorio"}), 400
    resultado = coleccion.insert_one({"nombre": datos["nombre"]})
    nuevo = {"id": str(resultado.inserted_id), "nombre": datos["nombre"]}
    return jsonify(nuevo), 201



@app.delete("/usuarios/<id>")
def eliminar_usuario(id):
    try:
        resultado = coleccion.delete_one({"_id": ObjectId(id)})
    except InvalidId:
        return jsonify({"error": "ID inválido"}), 400
    if resultado.deleted_count == 0:
        return jsonify({"error": "Usuario no encontrado"}), 404

    # Avisar al servicio de tareas para que borre las tareas del usuario
    try:
        requests.delete(f"{SERVICIO_TAREAS}/tareas/usuario/{id}", timeout=3)
    except requests.exceptions.RequestException:
        pass  # Si tareas no responde, el usuario ya se eliminó igualmente

    return jsonify({"mensaje": "Usuario eliminado"})



@app.get("/health")
def health():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)