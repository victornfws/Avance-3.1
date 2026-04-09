import streamlit as st
import numpy as np
from collections import deque
import time
import re

def solve_maze(maze, start, end):
    start_time = time.time()
    queue = deque([(start, [start])])
    visited = {start}

    while queue:
        (r, c), path = queue.popleft()

        if (r, c) == end:
            return path, (time.time() - start_time)

        for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < maze.shape[0] and 0 <= nc < maze.shape[1]:
                if maze[nr, nc] != 1 and (nr, nc) not in visited:
                    visited.add((nr, nc))
                    queue.append(((nr, nc), path + [(nr, nc)]))

    return None, 0


st.title("Cargador de Laberintos")

archivo = st.file_uploader("Sube tu archivo .txt con el laberinto", type=["txt"])

if archivo:
    content = archivo.read().decode("utf-8")
    lines = content.strip().split('\n')
    maze_data = []

    for line in lines:
        row = [int(d) for d in re.findall(r'\d', line)]  # <-- fix aqui
        if row:
            maze_data.append(row)

    maze_np = np.array(maze_data)
    p2 = np.where(maze_np == 2)
    p3 = np.where(maze_np == 3)

    if p2[0].size > 0 and p3[0].size > 0:
        start = (int(p2[0][0]), int(p2[1][0]))
        end = (int(p3[0][0]), int(p3[1][0]))

        if st.button("Resolver Laberinto Cargado"):
            ruta, tiempo = solve_maze(maze_np, start, end)

            if ruta:
                st.success(f"Resuelto en {tiempo:.6f} segundos. Pasos: {len(ruta)}")

                for r in range(maze_np.shape[0]):
                    fila_str = ""
                    for c in range(maze_np.shape[1]):
                        if (r, c) == start:
                            fila_str += "🧑"
                        elif (r, c) == end:
                            fila_str += "🏁"
                        elif (r, c) in ruta:
                            fila_str += "⬛"
                        elif maze_np[r, c] == 1:
                            fila_str += "⬜"
                        else:
                            fila_str += "🔹"
                    st.text(fila_str)
            else:
                st.error("No se encontro una ruta valida.")
    else:
        st.warning("El archivo debe contener un '2' (inicio) y un '3' (fin).")
else:
    st.info("Esperando archivo...")