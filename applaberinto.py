import streamlit as st
import numpy as np
from collections import deque
import heapq
import time
import re

def solve_maze_bfs(maze, start, end):
    start_time = time.time()
    # Solo guardamos el nodo actual en la cola
    queue = deque([start])
    # parent nos servirá para reconstruir el camino y actuar como 'visited'
    parent = {start: None}
    
    found = False
    while queue:
        curr = queue.popleft()
        
        if curr == end:
            found = True
            break
            
        r, c = curr
        for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nr, nc = r + dr, c + dc
            
            if 0 <= nr < maze.shape[0] and 0 <= nc < maze.shape[1]:
                # Si no es pared y no lo hemos visitado
                if maze[nr, nc] != 1 and (nr, nc) not in parent:
                    parent[(nr, nc)] = curr
                    queue.append((nr, nc))
    
    if found:
        # Reconstruimos la ruta desde el final hacia atrás
        path = []
        paso = end
        while paso is not None:
            path.append(paso)
            paso = parent[paso]
        return path[::-1], (time.time() - start_time) # Volteamos la ruta
        
    return None, 0

def solve_maze_dfs(maze, start, end):
    start_time = time.time()
    stack = [start]
    parent = {start: None}
    while stack:
        r, c = stack.pop()
        if (r, c) == end:
            path = []
            paso = end
            while paso is not None:
                path.append(paso)
                paso = parent[paso]
            return path[::-1], (time.time() - start_time)
        for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < maze.shape[0] and 0 <= nc < maze.shape[1]:
                if maze[nr, nc] != 1 and (nr, nc) not in parent:
                    parent[(nr, nc)] = (r, c)
                    stack.append((nr, nc))
    return None, 0

def heuristica(a, b):
    # Distancia Manhattan: suma de diferencias absolutas en filas y columnas
    # Es admisible para grids con movimiento en 4 direcciones (nunca sobreestima)
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def solve_maze_astar(maze, start, end):
    start_time = time.time()

    # Cada entrada en el heap: (f, g, nodo, path)
    # f = g + h  →  costo real acumulado + estimacion heuristica al destino
    # g = pasos dados hasta ahora (costo uniforme, cada celda vale 1)
    h_inicial = heuristica(start, end)
    heap = [(h_inicial, 0, start, [start])]
    # g_costos guarda el menor costo conocido para llegar a cada nodo
    g_costos = {start: 0}

    while heap:
        f, g, (r, c), path = heapq.heappop(heap)

        if (r, c) == end:
            return path, (time.time() - start_time)

        # Si ya encontramos un camino mas barato a este nodo, ignorar
        if g > g_costos.get((r, c), float('inf')):
            continue

        for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < maze.shape[0] and 0 <= nc < maze.shape[1]:
                if maze[nr, nc] != 1:
                    nuevo_g = g + 1
                    if nuevo_g < g_costos.get((nr, nc), float('inf')):
                        g_costos[(nr, nc)] = nuevo_g
                        nuevo_f = nuevo_g + heuristica((nr, nc), end)
                        heapq.heappush(heap, (nuevo_f, nuevo_g, (nr, nc), path + [(nr, nc)]))

    return None, 0

def render_maze(maze_np, start, end, ruta_set=None):
    filas = []
    for r in range(maze_np.shape[0]):
        fila_str = ""
        for c in range(maze_np.shape[1]):
            if (r, c) == start:
                fila_str += "🧑"
            elif (r, c) == end:
                fila_str += "🏁"
            elif ruta_set and (r, c) in ruta_set:
                fila_str += "🔹"
            elif maze_np[r, c] == 1:
                fila_str += "⬜"
            else:
                fila_str += "⬛"
        filas.append(fila_str)
    for fila in filas:
        st.text(fila)

st.title("Visualizador de Algoritmo de Busqueda de Laberinto")

st.sidebar.header("Opciones")
algorithm = st.sidebar.selectbox("Selecciona el algoritmo", ["BFS", "DFS", "A*"])
archivo = st.sidebar.file_uploader("Cargar laberinto (.txt)", type=["txt"])
solve_button = st.sidebar.button("Resolver Laberinto")

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
            if algorithm == "BFS":
                ruta, tiempo = solve_maze_bfs(maze_np, start, end)
            elif algorithm == "DFS":
                ruta, tiempo = solve_maze_dfs(maze_np, start, end)
            elif algorithm == "A*":
                ruta, tiempo = solve_maze_astar(maze_np, start, end)
            else:
                ruta = None

            if ruta:
                ruta_set = set(ruta)
                st.success(f"[{algorithm}] Resuelto en {tiempo:.6f} segundos. Casillas recorridas: {len(ruta)}")
                render_maze(maze_np, start, end, ruta_set)
            else:
                st.error("No se encontro una ruta valida.")
                render_maze(maze_np, start, end)
        else:
            render_maze(maze_np, start, end)
    else:
        st.warning("El archivo debe contener un '2' (inicio) y un '3' (fin).")
else:
    st.info("Esperando archivo...")