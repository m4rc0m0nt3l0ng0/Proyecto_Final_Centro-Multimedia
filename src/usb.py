import tkinter as tk
from PIL import Image, ImageTk
from threading import Thread
from queue import Queue
from screeninfo import get_monitors
from image_slideshow import ImageSlideshow
from audio_usb import AudioUSB
from video_usb import VideoUSB
from media_manager import MediaManager

class USBInterface:
    """
    Clase para gestionar la interfaz de dispositivos USB.
    Permite detectar archivos multimedia, actualizarlos dinámicamente y ejecutar acciones específicas.
    """
    def __init__(self, root, volver_callback):
        """
        Inicializa la interfaz USB y sus componentes.
        """
        self.root = root
        self.volver_callback = volver_callback
        self.current_frame = None
        self.media_manager = MediaManager()
        self.queue = Queue()
        self.hilo_dispositivo = Thread(target=self.media_manager.monitor_devices, args=(self.queue,), daemon=True)
        self.hilo_dispositivo.start()
        self.imagenes = []
        self.audio_files = []
        self.video_files = []
        self.buttons = {}

    def limpiar_frame(self):
        """
        Elimina el frame actual de la interfaz.
        """
        if self.current_frame:
            for widget in self.current_frame.winfo_children():
                widget.destroy()
            self.current_frame.destroy()
            self.current_frame = None

    def mostrar_interfaz_usb(self):
        """
        Configura y muestra la interfaz gráfica de USB.
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

        barra_sup = tk.Label(self.current_frame, bg="#003264", fg="white", font=("Arial", 24), text="USB")
        barra_sup.place(x=0, y=0, width=screen_width, height=screen_height // 10)

        mensaje_label = tk.Label(
            self.current_frame,
            text="Selecciona los archivos",
            font=("Arial", 18),
            fg="white",
            bg="#003264"
        )
        mensaje_label.place(x=0, y=screen_height // 10, width=screen_width)

        volver_btn = tk.Button(
            self.current_frame,
            text="Volver",
            font=("Arial", 12),
            bg="#00FFFF",
            fg="black",
            command=self.volver_callback
        )
        volver_btn.place(x=10, y=15, width=screen_width // 10, height=screen_height // 20)

        barra_inf = tk.Label(
            self.current_frame,
            text="Marco, Monse & Leo",
            bg="#003264",
            fg="white",
            font=("Arial", 12)
        )
        barra_inf.place(x=0, y=screen_height - screen_height // 15, width=screen_width, height=screen_height // 15)

        self.crear_botones_usb(screen_width, screen_height)
        self.actualizar_interfaz_usb()

    def crear_botones_usb(self, screen_width, screen_height):
        """
        Crea los botones para las funcionalidades de manejo de USB.
        """
        botones = [
            {"path": "img_interfaz/Fotos.png", "label": "Fotos"},
            {"path": "img_interfaz/Video.png", "label": "Video"},
            {"path": "img_interfaz/Musica.png", "label": "Música"},
        ]
        button_width = screen_width // 6
        button_height = screen_height // 6
        margin_x = screen_width // 40
        x_start = (screen_width - (len(botones) * button_width + (len(botones) - 1) * margin_x)) // 2
        y_start = screen_height // 3

        for i, boton in enumerate(botones):
            img = Image.open(boton["path"]).resize((button_width, button_height), Image.Resampling.LANCZOS)
            boton_img = ImageTk.PhotoImage(img)
            button = tk.Button(
                self.current_frame,
                image=boton_img,
                text=boton["label"],
                compound="top",
                bg="#00FFFF",
                fg="black",
                font=("Arial", 10),
                state="disabled",
                command=lambda label=boton["label"]: self.accion_boton(label)
            )
            button.image = boton_img
            button.place(x=x_start + i * (button_width + margin_x), y=y_start, width=button_width, height=button_height)
            self.buttons[boton["label"]] = button

    def accion_boton(self, label):
        """
        Realiza la acción correspondiente al botón seleccionado.
        """
        nueva_ventana = tk.Toplevel(self.root)
        nueva_ventana.title(label)
        nueva_ventana.geometry(f"{self.root.winfo_screenwidth()}x{self.root.winfo_screenheight()}")

        if label == "Fotos":
            if self.imagenes:
                slideshow = ImageSlideshow(nueva_ventana, self.imagenes, nueva_ventana.destroy)
                slideshow.mostrar_presentacion()
            else:
                tk.Label(
                    nueva_ventana, 
                    text="No se encontraron imágenes.", 
                    font=("Arial", 16), 
                    fg="red"
                ).pack(pady=20)
        elif label == "Música":
            if self.audio_files:
                AudioUSB(nueva_ventana, nueva_ventana.destroy, self.audio_files)
            else:
                tk.Label(
                    nueva_ventana, 
                    text="No se encontraron archivos de música.", 
                    font=("Arial", 16), 
                    fg="red"
                ).pack(pady=20)
        elif label == "Video":
            if self.video_files:
                VideoUSB(nueva_ventana, nueva_ventana.destroy, self.video_files)
            else:
                tk.Label(
                    nueva_ventana, 
                    text="No se encontraron archivos de video.", 
                    font=("Arial", 16), 
                    fg="red"
                ).pack(pady=20)

    def actualizar_interfaz_usb(self):
        """
        Actualiza el estado de la interfaz según los dispositivos conectados.
        """
        try:
            while not self.queue.empty():
                action, images, audio_files, video_files = self.queue.get()

                if action == "add":
                    self.imagenes = images
                    self.audio_files = audio_files
                    self.video_files = video_files

                    self.buttons["Fotos"].config(state="normal" if images else "disabled")
                    self.buttons["Música"].config(state="normal" if audio_files else "disabled")
                    self.buttons["Video"].config(state="normal" if video_files else "disabled")
                elif action == "remove":
                    self.imagenes.clear()
                    self.audio_files.clear()
                    self.video_files.clear()

                    for button in self.buttons.values():
                        button.config(state="disabled")
        except Exception as e:
            print(f"Error al actualizar la interfaz: {e}")

        self.root.after(1000, self.actualizar_interfaz_usb)
