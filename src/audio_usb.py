import tkinter as tk
from PIL import Image, ImageTk
import vlc
from screeninfo import get_monitors

class AudioUSB:
    """
    Clase para gestionar un reproductor de música basado en GUI.
    Permite cargar canciones, controlarlas y manejar la interfaz gráfica.
    """
    def __init__(self, root, volver_callback, canciones):
        """
        Inicializa los parámetros del reproductor, la interfaz y el manejo de canciones.
        """
        self.root = root
        self.volver_callback = volver_callback
        self.canciones = canciones
        self.current_song_index = 0

        self.player = vlc.MediaPlayer()
        self.timer_id = None
        self.remaining_time = 0

        self.current_frame = None
        self.mostrar_interfaz_audio()

    def limpiar_frame(self):
        """
        Limpia la interfaz actual y detiene cualquier reproducción activa.
        """
        if self.player.is_playing():
            self.player.stop()
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
            self.timer_id = None
        if self.current_frame:
            for widget in self.current_frame.winfo_children():
                widget.destroy()
            self.current_frame.destroy()
            self.current_frame = None

    def mostrar_interfaz_audio(self):
        """
        Configura la interfaz gráfica para la reproducción de música.
        """
        self.limpiar_frame()
        monitor = get_monitors()[0]
        screen_width = monitor.width
        screen_height = monitor.height

        self.current_frame = tk.Frame(self.root)
        self.current_frame.pack(fill="both", expand=True)

        fondo_img = Image.open("img_interfaz/Fondo.jpg").resize((screen_width, screen_height), Image.Resampling.LANCZOS)
        fondo = ImageTk.PhotoImage(fondo_img)
        fondo_label = tk.Label(self.current_frame, image=fondo)
        fondo_label.image = fondo
        fondo_label.place(x=0, y=0, relwidth=1, relheight=1)

        barra_sup = tk.Label(self.current_frame, bg="#003264", fg="white", font=("Arial", 24), text="Reproductor de Música")
        barra_sup.place(x=0, y=0, width=screen_width, height=screen_height // 10)

        barra_inf = tk.Label(self.current_frame, text="Marco, Monse & Leo", bg="#003264", fg="white", font=("Arial", 12))
        barra_inf.place(x=0, y=screen_height - screen_height // 15, width=screen_width, height=screen_height // 15)

        self.song_title_label = tk.Label(self.current_frame, text="", font=("Arial", 18), fg="white", bg="#003264")
        self.song_title_label.place(x=0, y=screen_height // 10, width=screen_width)

        try:
            img_size = min(screen_width // 6, screen_height // 6)
            img = Image.open("img_interfaz/cancion.png").resize((img_size, img_size), Image.Resampling.LANCZOS)
            self.song_img = ImageTk.PhotoImage(img)
            song_img_label = tk.Label(self.current_frame, image=self.song_img, bg="#003264")
            song_img_label.place(x=(screen_width - img_size) // 2, y=screen_height // 4)
        except Exception as e:
            print(f"Error al cargar la imagen: {e}")

        self.crear_botones(screen_width, screen_height)
        self.reproducir_cancion()

    def crear_botones(self, screen_width, screen_height):
        """
        Crea los botones de control para manejar la reproducción.
        """
        button_config = [
            {"text": "Anterior", "command": self.cancion_anterior},
            {"text": "Reanudar", "command": self.reanudar_cancion},
            {"text": "Pausar", "command": self.pausar_cancion},
            {"text": "Siguiente", "command": self.siguiente_cancion},
            {"text": "Volver", "command": self.volver},
        ]

        button_width = screen_width // 10
        button_height = screen_height // 15
        margin_x = screen_width // 40
        x_start = (screen_width - (len(button_config) * button_width + (len(button_config) - 1) * margin_x)) // 2
        y_pos = screen_height // 2

        for i, btn in enumerate(button_config):
            tk.Button(
                self.current_frame,
                text=btn["text"],
                font=("Arial", 12),
                bg="#00FFFF",
                fg="black",
                command=btn["command"]
            ).place(x=x_start + i * (button_width + margin_x), y=y_pos, width=button_width, height=button_height)

    def reproducir_cancion(self):
        """
        Inicia la reproducción de la canción seleccionada y configura un temporizador.
        """
        if self.canciones and 0 <= self.current_song_index < len(self.canciones):
            song_path = self.canciones[self.current_song_index]
            media = vlc.Media(song_path)
            self.player.set_media(media)
            self.player.play()
            self.song_title_label.config(text=f"Reproduciendo: {song_path.split('/')[-1]}")
            self.root.after(1000, self.iniciar_temporizador)

    def iniciar_temporizador(self):
        """
        Configura un temporizador para el cambio de canción.
        """
        duracion = self.player.get_length()
        if duracion > 0:
            self.remaining_time = duracion
            self.timer_id = self.root.after(self.remaining_time, self.siguiente_cancion)
        else:
            self.root.after(1000, self.iniciar_temporizador)

    def pausar_temporizador(self):
        """
        Detiene el temporizador actual.
        """
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
            self.timer_id = None

    def reanudar_temporizador(self):
        """
        Reanuda el temporizador pausado.
        """
        if self.remaining_time > 0:
            self.timer_id = self.root.after(self.remaining_time, self.siguiente_cancion)

    def siguiente_cancion(self):
        """
        Avanza a la siguiente canción de la lista.
        """
        self.pausar_temporizador()
        if self.canciones:
            self.current_song_index = (self.current_song_index + 1) % len(self.canciones)
            self.reproducir_cancion()

    def cancion_anterior(self):
        """
        Retrocede a la canción anterior en la lista.
        """
        self.pausar_temporizador()
        if self.canciones:
            self.current_song_index = (self.current_song_index - 1) % len(self.canciones)
            self.reproducir_cancion()

    def pausar_cancion(self):
        """
        Pausa la canción en reproducción.
        """
        self.player.pause()
        if self.timer_id:
            self.remaining_time -= 1000
        self.pausar_temporizador()

    def reanudar_cancion(self):
        """
        Reanuda la canción pausada.
        """
        self.player.play()
        self.reanudar_temporizador()

    def volver(self):
        """
        Regresa a la interfaz anterior definida por el callback.
        """
        self.limpiar_frame()
        self.volver_callback()
