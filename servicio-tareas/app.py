import requests
import os
from flask import Flask, jsonify, request
from flask_cors import CORS
from pymongo import MongoClient
from bson import ObjectId
from bson.errors import InvalidId

app = Flask(__name__)
CORS(app)

MONGO_URI = os.environ.get("MONGO_URI", "mongodb://localhost:27017")
#SERVICIO_USUARIOS = "http://localhost:5001"
SERVICIO_USUARIOS = os.environ.get("SERVICIO_USUARIOS", "http://localhost:5001")

cliente = MongoClient(MONGO_URI)
db = cliente["tareas_db"]
coleccion = db["tareas"]


def serializar(tarea):
    return {
        "id": str(tarea["_id"]),
        "titulo": tarea["titulo"],
        "usuario_id": tarea["usuario_id"],
        "completada": tarea.get("completada", False),
    }


def usuario_existe(usuario_id):
    """Consulta al servicio de usuarios si el usuario existe."""
    try:
        r = requests.get(f"{SERVICIO_USUARIOS}/usuarios/{usuario_id}", timeout=3)
        return r.status_code == 200
    except requests.exceptions.RequestException:
        return None  # El servicio de usuarios no responde


@app.get("/tareas")
def listar_tareas():
    tareas = [serializar(t) for t in coleccion.find()]
    return jsonify(tareas)


@app.post("/tareas")
def crear_tarea():
    datos = request.get_json()
    if not datos or not datos.get("titulo") or not datos.get("usuario_id"):
        return jsonify({"error": "titulo y usuario_id son obligatorios"}), 400

    existe = usuario_existe(datos["usuario_id"])
    if existe is None:
        return jsonify({"error": "Servicio de usuarios no disponible"}), 503
    if not existe:
        return jsonify({"error": "El usuario no existe"}), 404

    nueva = {
        "titulo": datos["titulo"],
        "usuario_id": datos["usuario_id"],
        "completada": False,
    }
    resultado = coleccion.insert_one(nueva)
    nueva["_id"] = resultado.inserted_id
    return jsonify(serializar(nueva)), 201


@app.patch("/tareas/<id>")
def completar_tarea(id):
    try:
        resultado = coleccion.update_one(
            {"_id": ObjectId(id)}, {"$set": {"completada": True}}
        )
    except InvalidId:
        return jsonify({"error": "ID inválido"}), 400
    if resultado.matched_count == 0:
        return jsonify({"error": "Tarea no encontrada"}), 404
    return jsonify({"mensaje": "Tarea completada"})

@app.delete("/tareas/<id>")
def eliminar_tarea(id):
    try:
        resultado = coleccion.delete_one({"_id": ObjectId(id)})
    except InvalidId:
        return jsonify({"error": "ID inválido"}), 400
    if resultado.deleted_count == 0:
        return jsonify({"error": "Tarea no encontrada"}), 404
    return jsonify({"mensaje": "Tarea eliminada"})


@app.delete("/tareas/usuario/<usuario_id>")
def eliminar_tareas_de_usuario(usuario_id):
    resultado = coleccion.delete_many({"usuario_id": usuario_id})
    return jsonify({"eliminadas": resultado.deleted_count})


@app.get("/health")
def health():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002, debug=True)