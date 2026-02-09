import tkinter as tk
import customtkinter as ctk
import random

# Configuración
# Modos: "System" (estándar), "Dark" (oscuro), "Light" (claro)
ctk.set_appearance_mode("System")
# Temas: "blue" (estándar), "green", "dark-blue"
ctk.set_default_color_theme("blue")

class Palabras_a_tiempo(ctk.CTk):
    """
    Clase Principal del Juego que maneja la interfaz de usuario (UI) y la lógica de Alphabet Sprint.
    Hereda de customtkinter.CTk.
    """
    def __init__(self):
        """Inicializa la ventana principal y las variables de estado del juego."""
        super().__init__()

        # Configuración de la Ventana
        self.title("Palabras a Tiempo")
        self.geometry("900x600")
        
        # Estado del Juego
        self.jugadores = []              # Lista de jugadores (diccionarios con nombre y estado)
        self.indice_jugador_actual = 0  # Índice del jugador actual
        self.temas = [                # Lista de temáticas disponibles
            "Animales", "Paises", "Frutas", "Colores", "Profesiones",
            "Deportes", "Instrumentos", "Ropa", "Comida", "Tecnología"
        ]
        self.tema_actual = ""        # Temática actual seleccionada
        self.letras_usadas = set()      # Conjunto de letras ya usadas en la ronda
        self.letra_seleccionada = None    # Letra seleccionada actualmente por el usuario
        self.temporizador_activo = False     # Estado del temporizador
        self.tiempo_restante = 15            # Tiempo restante en segundos

        # Inicialización de la Interfaz
        self.pantallas = {}
        self.configurar_frames()
        self.mostrar_pantalla("Configuracion")

    def configurar_frames(self):
        """Crea los contenedores (frames) para las diferentes pantallas del juego."""
        self.contenedor = ctk.CTkFrame(self)
        self.contenedor.pack(fill="both", expand=True)
        
        # Pantalla de Configuración
        self.frame_configuracion = ctk.CTkFrame(self.contenedor)
        self.pantallas["Configuracion"] = self.frame_configuracion
        self.crear_pantalla_configuracion()

        # Pantalla de Selección de Tema
        self.frame_tema = ctk.CTkFrame(self.contenedor)
        self.pantallas["Tema"] = self.frame_tema
        self.crear_pantalla_tema()

        # Pantalla de Juego
        self.frame_juego = ctk.CTkFrame(self.contenedor)
        self.pantallas["Juego"] = self.frame_juego
        self.crear_pantalla_juego()

    def mostrar_pantalla(self, nombre_pantalla):
        """
        Cambia la pantalla visible a la especificada.
        
        Parámetros:
            nombre_pantalla (str): El nombre de la pantalla ("Configuracion", "Tema", "Juego").
        """
        frame = self.pantallas[nombre_pantalla]
        frame.tkraise()
        # Ocultar los otros frames
        for nombre, f in self.pantallas.items():
            if nombre == nombre_pantalla:
                f.pack(fill="both", expand=True)
            else:
                f.pack_forget()

    def crear_pantalla_configuracion(self):
        """Crea la pantalla de configuración de jugadores con inputs dinámicos."""
        self.frame_configuracion.grid_columnconfigure(0, weight=1)
        
        titulo = ctk.CTkLabel(self.frame_configuracion, text="Palabras a Tiempo", font=("Arial", 32, "bold"))
        titulo.pack(pady=30)
        
        # Frame desplazable en caso de agregar muchos jugadores
        self.contenedor_jugadores = ctk.CTkScrollableFrame(self.frame_configuracion, height=300, width=400)
        self.contenedor_jugadores.pack(pady=10)

        self.entradas_jugadores = []
        self.configurar_inputs_jugadores(cantidad_inicial=2)

        # Área de Botones
        frame_botones = ctk.CTkFrame(self.frame_configuracion, fg_color="transparent")
        frame_botones.pack(pady=20)

        boton_agregar = ctk.CTkButton(frame_botones, text="+ Agregar", command=self.agregar_input_jugador, width=100)
        boton_agregar.pack(side="left", padx=5)
        
        boton_quitar = ctk.CTkButton(frame_botones, text="- Quitar", command=self.eliminar_input_jugador, width=100, fg_color="red", hover_color="darkred")
        boton_quitar.pack(side="left", padx=5)
        
        boton_siguiente = ctk.CTkButton(frame_botones, text="Siguiente >", command=self.ir_a_seleccion_tema, width=100, fg_color="green", hover_color="darkgreen")
        boton_siguiente.pack(side="left", padx=5)

    def configurar_inputs_jugadores(self, cantidad_inicial):
        """
        Genera los inputs iniciales para los jugadores.
        
        Parámetros:
            cantidad_inicial (int): Número inicial de campos de entrada.
        """
        for _ in range(cantidad_inicial):
            self.agregar_input_jugador()

    def agregar_input_jugador(self, evento=None):
        """
        Agrega un nuevo campo de entrada para un jugador.
        
        Parámetros:
            evento (opcional): Evento del teclado si se llama vía bind (Enter).
        """
        if len(self.entradas_jugadores) >= 8: # Límite máximo de jugadores
            return

        conteo = len(self.entradas_jugadores) + 1
        entrada = ctk.CTkEntry(self.contenedor_jugadores, placeholder_text=f"Nombre Jugador {conteo}")
        entrada.pack(pady=5)
        # Asociar tecla Enter para agregar otro jugador rápidamente
        entrada.bind("<Return>", self.agregar_input_jugador)
        
        self.entradas_jugadores.append(entrada)
        entrada.focus() # Poner el foco en el nuevo campo

    def eliminar_input_jugador(self):
        """Elimina el último campo de entrada de jugador."""
        if len(self.entradas_jugadores) <= 1: # Mantener al menos 1 jugador
            return
            
        entrada_a_eliminar = self.entradas_jugadores.pop()
        entrada_a_eliminar.destroy()

    def crear_pantalla_tema(self):
        """Crea la pantalla de selección de temática."""
        self.frame_tema.grid_columnconfigure(0, weight=1)
        self.frame_tema.grid_rowconfigure((0, 4), weight=1) # Centrar verticalmente

        titulo = ctk.CTkLabel(self.frame_tema, text="Elegir Temática", font=("Arial", 28, "bold"))
        titulo.pack(pady=40)

        self.label_tema_seleccionado = ctk.CTkLabel(self.frame_tema, text="...", font=("Arial", 40, "bold"), text_color="#3B8ED0")
        self.label_tema_seleccionado.pack(pady=30)

        frame_botones = ctk.CTkFrame(self.frame_tema, fg_color="transparent")
        frame_botones.pack(pady=40)

        boton_cambiar = ctk.CTkButton(frame_botones, text="Cambiar Tema", command=self.elegir_tema_aleatorio)
        boton_cambiar.pack(side="left", padx=20)

        boton_inicio = ctk.CTkButton(frame_botones, text="Comenzar Juego", command=self.iniciar_juego, fg_color="green", hover_color="darkgreen")
        boton_inicio.pack(side="left", padx=20)

    def elegir_tema_aleatorio(self):
        """Selecciona un tema aleatorio de la lista y actualiza la etiqueta display."""
        self.tema_actual = random.choice(self.temas)
        self.label_tema_seleccionado.configure(text=self.tema_actual)

    def ir_a_seleccion_tema(self):
        """Valida la entrada de jugadores y avanza a la selección de tema."""
        self.jugadores = []
        for entrada in self.entradas_jugadores:
            nombre = entrada.get().strip()
            if nombre:
                self.jugadores.append({"nombre": nombre, "activo": True})
        
        if len(self.jugadores) < 1:
             # Fallback de seguridad
             self.jugadores.append({"nombre": "Jugador 1", "activo": True})

        self.elegir_tema_aleatorio()
        self.mostrar_pantalla("Tema")

    def iniciar_juego(self):
        """Inicializa el estado del juego y cambia a la pantalla principal de juego."""
        self.label_tema.configure(text=f"Temática: {self.tema_actual}")
        self.indice_jugador_actual = 0  # Reiniciar al primer jugador
        self.actualizar_etiqueta_jugador()
        
        self.mostrar_pantalla("Juego")
        self.iniciar_turno()

    def crear_pantalla_juego(self):
        """Crea la interfaz principal del juego (tablero, temporizador, grid)."""
        # Barra Superior
        self.barra_superior = ctk.CTkFrame(self.frame_juego, height=50)
        self.barra_superior.pack(fill="x", padx=10, pady=5)
        
        self.label_tema = ctk.CTkLabel(self.barra_superior, text="Temática: ---", font=("Arial", 16))
        self.label_tema.pack(side="left", padx=20)
        
        self.label_jugador = ctk.CTkLabel(self.barra_superior, text="Turno de: ---", font=("Arial", 16, "bold"))
        self.label_jugador.pack(side="right", padx=20)

        # Temporizador
        self.label_temporizador = ctk.CTkLabel(self.frame_juego, text="15", font=("Arial", 48, "bold"), text_color="red")
        self.label_temporizador.pack(pady=10)

        # Contenedor de la Grilla (Abecedario)
        self.frame_grilla = ctk.CTkFrame(self.frame_juego)
        self.frame_grilla.pack(pady=10, padx=20)
        
        self.botones_letras = {}
        letras = "ABCDEFGHIJKLMNÑOPQRSTUVWXYZ"
        
        # Diseño de grilla 9 columnas x 3 filas
        for i, char in enumerate(letras):
            btn = ctk.CTkButton(self.frame_grilla, text=char, width=40, height=40,
                                command=lambda c=char: self.seleccionar_letra(c))
            fila = i // 9
            columna = i % 9
            btn.grid(row=fila, column=columna, padx=5, pady=5)
            self.botones_letras[char] = btn

        # Área de Entrada
        self.frame_input = ctk.CTkFrame(self.frame_juego)
        self.frame_input.pack(pady=20)
        
        self.entrada_palabra = ctk.CTkEntry(self.frame_input, placeholder_text="Escribe tu palabra aquí...")
        self.entrada_palabra.pack(side="left", padx=10)
        # Asociar Enter para enviar la palabra
        self.entrada_palabra.bind("<Return>", lambda event: self.enviar_palabra())
        
        self.boton_enviar = ctk.CTkButton(self.frame_input, text="Enviar", command=self.enviar_palabra)
        self.boton_enviar.pack(side="left", padx=10)

        self.label_estado = ctk.CTkLabel(self.frame_juego, text="", font=("Arial", 14))
        self.label_estado.pack(pady=5)

    def actualizar_etiqueta_jugador(self):
        """Actualiza la etiqueta con el nombre del jugador actual."""
        if self.jugadores:
            j = self.jugadores[self.indice_jugador_actual]
            self.label_jugador.configure(text=f"Turno de: {j['nombre']}")

    def seleccionar_letra(self, letra):
        """
        Maneja la selección de una letra en la grilla.
        
        Parámetros:
            letra (str): La letra seleccionada.
        """
        if letra in self.letras_usadas:
            self.label_estado.configure(text=f"La letra {letra} ya fue usada.", text_color="orange")
            return
            
        self.letra_seleccionada = letra
        # Resetear colores y resaltar la seleccionada
        for l, btn in self.botones_letras.items():
            if l not in self.letras_usadas:
                btn.configure(fg_color=["#3B8ED0", "#1F6AA5"])  # Color por defecto
        
        self.botones_letras[letra].configure(fg_color="green")
        self.label_estado.configure(text=f"Letra seleccionada: {letra}", text_color="blue")
        self.entrada_palabra.focus()

    def iniciar_turno(self):
        """Inicia el turno para el jugador actual."""
        if self.verificar_fin_juego():
            return

        self.letra_seleccionada = None
        self.entrada_palabra.delete(0, "end")
        self.label_estado.configure(text="Selecciona una letra y escribe una palabra.", text_color="black")
        
        # Resetear visuales de botones (excepto usados)
        for letra, btn in self.botones_letras.items():
            if letra in self.letras_usadas:
                btn.configure(state="disabled", fg_color="gray")
            else:
                btn.configure(state="normal", fg_color=["#3B8ED0", "#1F6AA5"])

        self.tiempo_restante = 15
        self.temporizador_activo = True
        self.actualizar_display_temporizador()
        self.cuenta_regresiva()

    def cuenta_regresiva(self):
        """Función recursiva para el temporizador."""
        if not self.temporizador_activo:
            return
            
        self.label_temporizador.configure(text=str(self.tiempo_restante))
        
        if self.tiempo_restante > 0:
            self.tiempo_restante -= 1
            self.after(1000, self.cuenta_regresiva)
        else:
            self.manejar_tiempo_agotado()

    def actualizar_display_temporizador(self):
        """Actualiza el widget de texto del temporizador."""
        self.label_temporizador.configure(text=str(self.tiempo_restante))

    def manejar_tiempo_agotado(self):
        """Elimina al jugador actual cuando se acaba el tiempo."""
        self.temporizador_activo = False
        jugador = self.jugadores[self.indice_jugador_actual]
        jugador["activo"] = False
        self.label_estado.configure(text=f"¡Tiempo fuera! {jugador['nombre']} eliminado.", text_color="red")
        
        # Pausa breve antes del siguiente turno
        self.after(2000, self.siguiente_turno)

    def enviar_palabra(self):
        """
        Valida y procesa la palabra enviada por el usuario.
        Verifica si comienza con la letra seleccionada.
        """
        if not self.temporizador_activo:
            return

        palabra = self.entrada_palabra.get().strip().upper()
        
        if not self.letra_seleccionada:
            self.label_estado.configure(text="¡Debes seleccionar una letra primero!", text_color="red")
            return
            
        if not palabra:
            self.label_estado.configure(text="¡Escribe una palabra!", text_color="red")
            return

        if not palabra.startswith(self.letra_seleccionada):
            self.label_estado.configure(text=f"La palabra debe empezar con {self.letra_seleccionada}", text_color="red")
            return

        # Camino exitoso
        self.temporizador_activo = False  # Detener temporizador
        self.letras_usadas.add(self.letra_seleccionada)
        self.botones_letras[self.letra_seleccionada].configure(state="disabled", fg_color="gray")
        
        self.label_estado.configure(text="¡Correcto!", text_color="green")
        
        # Verificar si se completó la ronda (todas las letras usadas)
        if len(self.letras_usadas) == len(self.botones_letras):
            self.label_estado.configure(text="¡Ronda completada! Reiniciando tablero...", text_color="blue")
            self.letras_usadas.clear()
            self.after(2000, self.siguiente_turno)
        else:
            self.after(1000, self.siguiente_turno)

    def siguiente_turno(self):
        """Avanza al siguiente jugador activo."""
        if self.verificar_fin_juego():
            return
            
        # Buscar siguiente jugador activo
        intentos = 0
        while intentos < len(self.jugadores):
            self.indice_jugador_actual = (self.indice_jugador_actual + 1) % len(self.jugadores)
            if self.jugadores[self.indice_jugador_actual]["activo"]:
                break
            intentos += 1
            
        self.actualizar_etiqueta_jugador()
        self.iniciar_turno()

    def verificar_fin_juego(self):
        """
        Verifica si el juego ha terminado basándose en los jugadores activos.
        Retorna True si el juego terminó.
        """
        jugadores_activos = [j for j in self.jugadores if j["activo"]]
        
        # Lógica: Si empezamos con > 1 jugador, paramos cuando queda 1 (Ganador).
        # Si empezamos con 1 jugador (Modo Solitario), paramos cuando quedan 0.
        umbral = 1 if len(self.jugadores) > 1 else 0
        
        if len(jugadores_activos) <= umbral:
            self.temporizador_activo = False
            
            if len(jugadores_activos) == 1:
                texto_ganador = f"¡Ganador: {jugadores_activos[0]['nombre']}!"
                color = "green"
            else:
                texto_ganador = "Juego Terminado"
                color = "red"
                
            self.label_estado.configure(text=texto_ganador, text_color=color, font=("Arial", 24, "bold"))
            self.label_temporizador.configure(text="FIN")
            
            # Deshabilitar entrada
            self.entrada_palabra.delete(0, "end")
            self.entrada_palabra.configure(state="disabled")
            self.boton_enviar.configure(state="disabled")
            return True
        return False

if __name__ == "__main__":
    app = Palabras_a_tiempo()
    app.mainloop()
