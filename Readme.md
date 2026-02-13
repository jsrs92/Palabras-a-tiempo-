# Palabras a tiempo

Un juego de mesa basado en el clásico tuttifrutti es llevado a la PC a través de la programación en Python.

## Descripción
**Palabras a tiempo** es un juego donde los jugadores deben ingresar palabras que comiencen con una letra seleccionada del tablero antes de que se acabe el tiempo.

## Requisitos
- Python 3.x instalado.
- Librería **customtkinter**, **tkinter**.

## Cómo Jugar

1.  Ejecuta el juego: `palabras_a_tiempo.py`
2.  Ingresa los nombres de los jugadores.
3.  Elige los temas. 
4.  Presiona "Iniciar Juego".
5.  El turno comienza para el primer jugador.
6.  **Objetivo**:
    -   Selecciona una letra disponible en la grilla.
    -   Escribe una palabra que comience con esa letra.
    -   Presiona "Enviar" o Enter antes de que el tiempo (15s) se agote.
7.  Si aciertas, la letra se bloquea y pasa el turno.
8.  Si se acaba el tiempo, el jugador es eliminado.
9.  ¡Gana el último jugador en pie!

## Reglas
-   La palabra debe comenzar obligatoriamente con la letra seleccionada.
-   No se pueden repetir letras en la misma ronda.
-   Si se completan todas las letras, el tablero se reinicia manteniendo el mismo tema hasta finalizar el juego.
