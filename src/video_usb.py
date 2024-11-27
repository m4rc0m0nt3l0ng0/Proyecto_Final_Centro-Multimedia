import tkinter as tk
from PIL import Image, ImageTk
import vlc
import platform
from screeninfo import get_monitors


class VideoUSB:
    """
    Clase para gestionar la selección y reproducción de videos desde un dispositivo USB.
    Permite la reproducción individual o en secuencia.
    """
    def __init__(self, root, volver_callback, videos):
        """
        Inicializa la interfaz de videos y la lista de videos disponibles.
        """
        self.root = root
        self.volver_callback = volver_callback
        self.videos = videos
        self.current_frame = None
        self.player = None
        self.current_video_index = 0
        self.presentacion_activa = False
        self.mostrar_interfaz_video()

    def limpiar_frame(self):
        """
        Limpia el frame actual y detiene la reproducción en curso.
        """
        if self.player and self.player.is_playing():
            self.player.stop()
        if self.current_frame:
            for widget in self.current_frame.winfo_children():
                widget.destroy()
            self.current_frame.destroy()
            self.current_frame = None

    def mostrar_interfaz_video(self):
        """
        Configura y muestra la interfaz gráfica de selección de videos.
        """
        self.limpiar_frame()
        self.current_frame = tk.Frame(self.root)
        self.current_frame.pack(fill="both", expand=True)

        monitor = get_monitors()[0]
        screen_width = monitor.width
        screen_height = monitor.height

        fondo_img = Image.open("img_interfaz/Fondo.jpg").resize((screen_width, screen_height), Image.Resampling.LANCZOS)
        fondo = ImageTk.PhotoImage(fondo_img)
        fondo_label = tk.Label(self.current_frame, image=fondo)
        fondo_label.image = fondo
        fondo_label.place(x=0, y=0, relwidth=1, relheight=1)

        barra_sup = tk.Label(
            self.current_frame,
            bg="#003264",
            fg="white",
            font=("Arial", 24),
            text="Videos"
        )
        barra_sup.place(x=0, y=0, width=screen_width, height=screen_height // 10)

        mensaje_label = tk.Label(
            self.current_frame,
            text="¿Qué video quieres ver?",
            font=("Arial", 18),
            fg="white",
            bg="#003264"
        )
        mensaje_label.place(x=0, y=screen_height // 10, width=screen_width)

        barra_inf = tk.Label(
            self.current_frame,
            text="Marco, Monse & Leo",
            bg="#003264",
            fg="white",
            font=("Arial", 12)
        )
        barra_inf.place(
            x=0,
            y=screen_height - screen_height // 15,
            width=screen_width,
            height=screen_height // 15
        )

        volver_btn = tk.Button(
            self.current_frame,
            text="Volver",
            font=("Arial", 12),
            bg="#00FFFF",
            fg="black",
            command=self.volver
        )
        volver_btn.place(x=10, y=15, width=screen_width // 10, height=screen_height // 20)

        self.crear_botones_videos(screen_width, screen_height)

        if len(self.videos) > 1:
            presentacion_btn = tk.Button(
                self.current_frame,
                text="Presentación",
                font=("Arial", 12),
                bg="#00FFFF",
                fg="black",
                command=self.iniciar_presentacion
            )
            presentacion_btn.place(
                x=screen_width - screen_width // 10 - 20,
                y=15,
                width=screen_width // 10,
                height=screen_height // 20
            )

    def crear_botones_videos(self, screen_width, screen_height):
        """
        Genera los botones para cada video disponible en la lista.
        """
        max_columns = 2
        button_width = screen_width // 4
        button_height = screen_height // 10
        margin_x = screen_width // 20
        margin_y = screen_height // 40
        start_x = (screen_width - max_columns * (button_width + margin_x)) // 2
        start_y = screen_height // 4

        for i, video in enumerate(self.videos):
            video_name = video.split("/")[-1]
            col = i % max_columns
            row = i // max_columns

            x_pos = start_x + col * (button_width + margin_x)
            y_pos = start_y + row * (button_height + margin_y)

            tk.Button(
                self.current_frame,
                text=video_name,
                font=("Arial", 10),
                bg="#00FFFF",
                fg="black",
                command=lambda v=video: self.reproducir_video(v)
            ).place(x=x_pos, y=y_pos, width=button_width, height=button_height)

    def reproducir_video(self, video_path):
        """
        Reproduce un video seleccionado en la pantalla.
        """
        self.limpiar_frame()
        self.current_frame = tk.Frame(self.root)
        self.current_frame.pack(fill="both", expand=True)

        monitor = get_monitors()[0]
        screen_width = monitor.width
        screen_height = monitor.height

        barra_sup = tk.Label(
            self.current_frame,
            bg="#003264",
            fg="white",
            font=("Arial", 24),
            text="Reproduciendo Video"
        )
        barra_sup.place(x=0, y=0, width=screen_width, height=screen_height // 10)

        volver_btn = tk.Button(
            self.current_frame,
            text="Regresar",
            font=("Arial", 12),
            bg="#00FFFF",
            fg="black",
            command=self.detener_video_y_volver
        )
        volver_btn.place(x=10, y=15, width=screen_width // 10, height=screen_height // 20)

        video_frame = tk.Frame(self.current_frame, bg="black")
        video_frame.place(x=0, y=screen_height // 10, width=screen_width, height=screen_height * 9 // 10)

        self.player = vlc.MediaPlayer(video_path)

        if platform.system() == "Linux":
            self.player.set_xwindow(video_frame.winfo_id())
        else:
            self.player.set_hwnd(video_frame.winfo_id())

        self.player.play()

        if self.presentacion_activa:
            self.player.event_manager().event_attach(
                vlc.EventType.MediaPlayerEndReached,
                self.siguiente_video_presentacion
            )

    def iniciar_presentacion(self):
        """
        Inicia la reproducción secuencial de todos los videos disponibles.
        """
        self.presentacion_activa = True
        self.current_video_index = 0
        self.reproducir_video(self.videos[self.current_video_index])

    def siguiente_video_presentacion(self, event=None):
        """
        Reproduce el siguiente video en la lista durante una presentación.
        """
        self.current_video_index += 1
        if self.current_video_index < len(self.videos):
            self.reproducir_video(self.videos[self.current_video_index])
        else:
            self.presentacion_activa = False
            self.mostrar_interfaz_video()

    def detener_video_y_volver(self):
        """
        Detiene la reproducción actual y regresa a la lista de videos.
        """
        if self.player and self.player.is_playing():
            self.player.stop()
        self.mostrar_interfaz_video()

    def volver(self):
        """
        Detiene cualquier reproducción y regresa a la interfaz anterior.
        """
        if self.player and self.player.is_playing():
            self.player.stop()
        self.limpiar_frame()
        self.volver_callback()
