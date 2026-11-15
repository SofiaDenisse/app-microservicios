# Gestor de tareas con microservicios

Aplicación web sencilla construida con arquitectura de microservicios.
Permite administrar usuarios y asignarles tareas.

## Arquitectura

```
Frontend (React) ──► API Gateway (5000) ──┬──► servicio-usuarios (5001) ──► usuarios_db
                                          └──► servicio-tareas   (5002) ──► tareas_db
```

| Componente | Tecnología | Puerto |
|---|---|---|
| frontend | React + Vite + Tailwind CSS | 5173 |
| gateway | Python + Flask | 5000 |
| servicio-usuarios | Python + Flask + PyMongo | 5001 |
| servicio-tareas | Python + Flask + PyMongo | 5002 |
| base de datos | MongoDB (una base por servicio) | 27017 |

El servicio de tareas consulta al de usuarios por HTTP para validar que
el usuario existe, y al eliminar un usuario se eliminan sus tareas.

## Requisitos

- Docker Desktop (opción recomendada), o bien:
- Python 3.10+, Node.js 18+ y MongoDB corriendo en `localhost:27017`

## Ejecución con Docker

```bash
docker compose up --build
```

Abre http://localhost:5173. Espera unos segundos a que el frontend termine de iniciar.

Para detener: `docker compose down` (agrega `-v` para borrar los datos).

## Ejecución sin Docker

Cada servicio en su propia terminal:

```bash
# Servicios Flask (repetir en servicio-usuarios, servicio-tareas y gateway)
cd servicio-usuarios
python -m venv venv
venv\Scripts\activate          # Linux/Mac: source venv/bin/activate
pip install -r requirements.txt
python app.py

# Frontend
cd frontend
npm install
npm run dev
```

## Endpoints principales (vía gateway)

| Método | Ruta | Descripción |
|---|---|---|
| GET | /api/usuarios | Listar usuarios |
| POST | /api/usuarios | Crear usuario |
| DELETE | /api/usuarios/:id | Eliminar usuario y sus tareas |
| GET | /api/tareas | Listar tareas |
| POST | /api/tareas | Crear tarea |
| PATCH | /api/tareas/:id | Marcar como completada |
| DELETE | /api/tareas/:id | Eliminar tarea |

## Autor

[Najera Garcia Sofia Denisse] - ESCOM, IPN