import streamlit as st
import numpy as np
from collections import deque
import heapq
import time
import re

# --- BFS ---
def solve_bfs(maze, start, end):
    start_time = time.time()
    queue = deque([(start, [start])])
    visited = {start}
    while queue:
        (r, c), path = queue.popleft()
        if (r, c) == end:
            return path, visited, (time.time() - start_time)
        for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < maze.shape[0] and 0 <= nc < maze.shape[1]:
                if maze[nr, nc] != 1 and (nr, nc) not in visited:
                    visited.add((nr, nc))
                    queue.append(((nr, nc), path + [(nr, nc)]))
    return None, visited, (time.time() - start_time)

# --- DFS ---
def solve_dfs(maze, start, end):
    start_time = time.time()
    stack = [(start, [start])]
    visited = set()
    while stack:
        (r, c), path = stack.pop()
        if (r, c) in visited:
            continue
        visited.add((r, c))
        if (r, c) == end:
            return path, visited, (time.time() - start_time)
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < maze.shape[0] and 0 <= nc < maze.shape[1]:
                if maze[nr, nc] != 1 and (nr, nc) not in visited:
                    stack.append(((nr, nc), path + [(nr, nc)]))
    return None, visited, (time.time() - start_time)

# --- A* ---
def solve_astar(maze, start, end):
    start_time = time.time()
    def h(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])
    open_set = [(h(start, end), 0, start, [start])]
    visited = set()
    g_score = {start: 0}
    while open_set:
        _, g, (r, c), path = heapq.heappop(open_set)
        if (r, c) in visited:
            continue
        visited.add((r, c))
        if (r, c) == end:
            return path, visited, (time.time() - start_time)
        for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < maze.shape[0] and 0 <= nc < maze.shape[1]:
                if maze[nr, nc] != 1 and (nr, nc) not in visited:
                    ng = g + 1
                    if ng < g_score.get((nr, nc), float('inf')):
                        g_score[(nr, nc)] = ng
                        heapq.heappush(open_set, (ng + h((nr, nc), end), ng, (nr, nc), path + [(nr, nc)]))
    return None, visited, (time.time() - start_time)

# --- Render ---
def render_maze(maze, start, end, path=None, visited=None):
    path = set(path) if path else set()
    visited = visited or set()
    filas = []
    for r in range(maze.shape[0]):
        fila_str = ""
        for c in range(maze.shape[1]):
            if (r, c) == start:
                fila_str += "🟢"
            elif (r, c) == end:
                fila_str += "🏁"
            elif (r, c) in path:
                fila_str += "🔹"
            elif (r, c) in visited:
                fila_str += "🟡"
            elif maze[r, c] == 1:
                fila_str += "⬜"
            else:
                fila_str += "⬛"
        filas.append(fila_str)
    st.text("\n".join(filas))

# --- UI ---
st.title("Visualizador de Algoritmos de Búsqueda en Laberinto")

st.sidebar.header("Opciones")
algorithm = st.sidebar.selectbox("Selecciona el algoritmo", ["BFS", "DFS", "A*"])
solve_button = st.sidebar.button("Resolver Laberinto")
archivo = st.sidebar.file_uploader("Cargar laberinto (.txt)", type=["txt"])

st.sidebar.markdown("""
**Iconos**
- 🧑 Inicio
- 🏁 Fin
- 🔹 Ruta final
- 🟪 Nodos explorados
- ⬜ Muro
- ⬛ Libre
""")

if archivo:
    content = archivo.read().decode("utf-8")
    lines = content.strip().split('\n')
    maze_data = []
    for line in lines:
        row = [int(d) for d in re.findall(r'\d', line)]
        if row:
            maze_data.append(row)

    maze_np = np.array(maze_data)
    p2 = np.where(maze_np == 2)
    p3 = np.where(maze_np == 3)

    if p2[0].size > 0 and p3[0].size > 0:
        start = (int(p2[0][0]), int(p2[1][0]))
        end   = (int(p3[0][0]), int(p3[1][0]))

        render_maze(maze_np, start, end)

        if solve_button:
            solvers = {"BFS": solve_bfs, "DFS": solve_dfs, "A*": solve_astar}
            path, visited, tiempo = solvers[algorithm](maze_np, start, end)

            if path:
                st.success(f"**{algorithm}** — Pasos: {len(path)} | Explorados: {len(visited)} | Tiempo: {tiempo:.6f}s")
                render_maze(maze_np, start, end, path, visited)
            else:
                st.error("No se encontró una ruta válida.")
    else:
        st.warning("El archivo debe contener un '2' (inicio) y un '3' (fin).")
else:
    st.info("Esperando archivo...")