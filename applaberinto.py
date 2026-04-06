import streamlit as st
import pandas as pd
from maze_solver import MAZE, START, END, solve_maze_bfs

st.title("Visualizador de Algoritmo de BÃºsqueda en Laberinto")

# FunciÃ³n para renderizar el laberinto
def render_maze(maze, path=None):
    if path is None:
        path = []
    
    # Convertir el laberinto a un formato que Streamlit pueda mostrar fÃ¡cilmente,
    # por ejemplo, una tabla o usando st.markdown con emojis/colores.
    # Para una mejor visualizaciÃ³n interactiva, podrÃ­as usar bibliotecas como Pygame o Plotly, 
    # pero para un inicio, un enfoque simple es suficiente.

    display_maze = []
    for r_idx, row in enumerate(maze):
        display_row = []
        for c_idx, col in enumerate(row):
            if (r_idx, c_idx) == START:
                display_row.append("ðŸš€") # Inicio
            elif (r_idx, c_idx) == END:
                display_row.append("ðŸ") # Fin
            elif (r_idx, c_idx) in path:
                display_row.append("ðŸ”¹") # Camino resuelto
            elif col == 1:
                display_row.append("â¬›") # Muro
            else:
                display_row.append("â¬œ") # Camino libre
        display_maze.append("".join(display_row))
    
    st.markdown("<br>".join(display_maze), unsafe_allow_html=True)


# Sidebar para controles
st.sidebar.header("Opciones")
algorithm = st.sidebar.selectbox("Selecciona el algoritmo", ["BFS", "DFS (no implementado)", "A* (no implementado)"])
solve_button = st.sidebar.button("Resolver Laberinto")

render_maze(MAZE)


if solve_button:
    if algorithm == "BFS":
        path = solve_maze_bfs(MAZE, START, END)
        if path:
           st.success(f"Â¡Camino encontrado con {algorithm}!")
           render_maze(MAZE, path)
        else:
            st.error("No se encontrÃ³ un camino.")
    else:
        st.warning(f"El algoritmo {algorithm} aÃºn no estÃ¡ implementado. Usa BFS.")
