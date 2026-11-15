import requests
import os
from flask import Flask, Response, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

SERVICIOS = {
    "usuarios": os.environ.get("SERVICIO_USUARIOS", "http://localhost:5001"),
    "tareas": os.environ.get("SERVICIO_TAREAS", "http://localhost:5002"),
}


def reenviar(servicio, ruta):
    url = f"{SERVICIOS[servicio]}/{ruta}"
    try:
        r = requests.request(
            method=request.method,
            url=url,
            json=request.get_json(silent=True),
            timeout=5,
        )
    except requests.exceptions.RequestException:
        return Response(
            f'{{"error": "Servicio de {servicio} no disponible"}}',
            status=503,
            content_type="application/json",
        )
    return Response(
        r.content,
        status=r.status_code,
        content_type=r.headers.get("Content-Type", "application/json"),
    )


@app.route("/api/usuarios", defaults={"ruta": ""}, methods=["GET", "POST", "DELETE"])
@app.route("/api/usuarios/<path:ruta>", methods=["GET", "POST", "DELETE"])
def usuarios(ruta):
    return reenviar("usuarios", f"usuarios/{ruta}".rstrip("/"))


@app.route("/api/tareas", defaults={"ruta": ""}, methods=["GET", "POST", "PATCH", "DELETE"])
@app.route("/api/tareas/<path:ruta>", methods=["GET", "POST", "PATCH", "DELETE"])
def tareas(ruta):
    return reenviar("tareas", f"tareas/{ruta}".rstrip("/"))


@app.get("/health")
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)