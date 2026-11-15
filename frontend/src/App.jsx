import { useEffect, useState } from "react";

const API_USUARIOS = "http://localhost:5000/api";
const API_TAREAS = "http://localhost:5000/api";

function App() {
  const [usuarios, setUsuarios] = useState([]);
  const [tareas, setTareas] = useState([]);
  const [nombre, setNombre] = useState("");
  const [titulo, setTitulo] = useState("");
  const [usuarioId, setUsuarioId] = useState("");
  const [error, setError] = useState("");

  const cargarUsuarios = async () => {
    try {
      const res = await fetch(`${API_USUARIOS}/usuarios`);
      if (!res.ok) throw new Error();
      setUsuarios(await res.json());
    } catch {
      setError("No se pudo conectar con el servicio de usuarios");
    }
  };

  const eliminarUsuario = async (id) => {
    await fetch(`${API_USUARIOS}/usuarios/${id}`, { method: "DELETE" });
    cargarUsuarios();
    cargarTareas();
  };

  const cargarTareas = async () => {
    try {
      const res = await fetch(`${API_TAREAS}/tareas`);
      if (!res.ok) throw new Error();
      setTareas(await res.json());
    } catch {
      setError("No se pudo conectar con el servicio de tareas");
    }
  };

  useEffect(() => {
    cargarUsuarios();
    cargarTareas();
  }, []);

  const crearUsuario = async (e) => {
    e.preventDefault();
    setError("");
    const res = await fetch(`${API_USUARIOS}/usuarios`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ nombre }),
    });
    if (!res.ok) {
      const data = await res.json();
      setError(data.error);
      return;
    }
    setNombre("");
    cargarUsuarios();
  };

  const crearTarea = async (e) => {
    e.preventDefault();
    setError("");
    const res = await fetch(`${API_TAREAS}/tareas`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ titulo, usuario_id: usuarioId }),
    });
    if (!res.ok) {
      const data = await res.json();
      setError(data.error);
      return;
    }
    setTitulo("");
    cargarTareas();
  };

  const completarTarea = async (id) => {
    await fetch(`${API_TAREAS}/tareas/${id}`, { method: "PATCH" });
    cargarTareas();
  };

  const eliminarTarea = async (id) => {
    await fetch(`${API_TAREAS}/tareas/${id}`, { method: "DELETE" });
    cargarTareas();
  };

  const nombreDeUsuario = (id) =>
    usuarios.find((u) => u.id === id)?.nombre ?? "Desconocido";

  const input =
    "flex-1 min-w-0 rounded-md border border-slate-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-200";
  const boton =
    "rounded-md bg-blue-600 px-3 py-2 text-sm font-medium text-white transition hover:bg-blue-700";

  return (
    <div className="min-h-screen bg-slate-100">
      <div className="mx-auto max-w-4xl p-6">
        <h1 className="mb-6 text-3xl font-bold text-slate-800">
          Gestor de tareas
        </h1>

        {error && (
          <p className="mb-4 rounded-md bg-red-100 px-4 py-2 text-sm text-red-700">
            {error}
          </p>
        )}

        <div className="grid gap-6 md:grid-cols-2">
          {/* Usuarios */}
          <section className="rounded-xl bg-white p-5 shadow">
            <h2 className="mb-4 text-xl font-semibold text-slate-700">
              Usuarios
            </h2>
            <form onSubmit={crearUsuario} className="mb-4 flex gap-2">
              <input
                className={input}
                value={nombre}
                onChange={(e) => setNombre(e.target.value)}
                placeholder="Nombre del usuario"
              />
              <button type="submit" className={boton}>
                Agregar
              </button>
            </form>
            <ul className="divide-y divide-slate-100">
              {usuarios.map((u) => (
                <li key={u.id} className="flex items-center justify-between py-2">
                  <span className="text-slate-700">{u.nombre}</span>
                  <button
                    onClick={() => eliminarUsuario(u.id)}
                    className="rounded-md bg-red-600 px-2 py-1 text-xs font-medium text-white transition hover:bg-red-700"
                  >
                    Eliminar
                  </button>
                </li>
              ))}
            </ul>
          </section>

          {/* Tareas */}
          <section className="rounded-xl bg-white p-5 shadow">
            <h2 className="mb-4 text-xl font-semibold text-slate-700">
              Tareas
            </h2>
            <form onSubmit={crearTarea} className="mb-4 flex flex-wrap gap-2">
              <input
                className={input}
                value={titulo}
                onChange={(e) => setTitulo(e.target.value)}
                placeholder="Título de la tarea"
              />
              <select
                className={input}
                value={usuarioId}
                onChange={(e) => setUsuarioId(e.target.value)}
                required
              >
                <option value="">Asignar a...</option>
                {usuarios.map((u) => (
                  <option key={u.id} value={u.id}>
                    {u.nombre}
                  </option>
                ))}
              </select>
              <button type="submit" className={boton}>
                Crear
              </button>
            </form>
            <ul className="divide-y divide-slate-100">
              {tareas.map((t) => (
                <li
                  key={t.id}
                  className="flex items-center justify-between gap-2 py-2"
                >
                  <span
                    className={
                      t.completada
                        ? "text-slate-400 line-through"
                        : "text-slate-700"
                    }
                  >
                    {t.titulo}{" "}
                    <small className="text-slate-400">
                      ({nombreDeUsuario(t.usuario_id)})
                    </small>
                  </span>
                  <div className="flex gap-2">
                    {!t.completada && (
                      <button
                        onClick={() => completarTarea(t.id)}
                        className="rounded-md bg-green-600 px-2 py-1 text-xs font-medium text-white transition hover:bg-green-700"
                      >
                        Completar
                      </button>
                    )}
                    <button
                      onClick={() => eliminarTarea(t.id)}
                      className="rounded-md bg-red-600 px-2 py-1 text-xs font-medium text-white transition hover:bg-red-700"
                    >
                      Eliminar
                    </button>
                  </div>
                </li>
              ))}
            </ul>
          </section>
        </div>
      </div>
    </div>
  );
}

export default App;