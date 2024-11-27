import tkinter as tk
from PIL import Image, ImageTk
from screeninfo import get_monitors
import subprocess
import os
import signal


class StreamingInterface:
    """
    Clase para gestionar la interfaz de Streaming.
    Permite abrir plataformas de streaming y controlar un navegador web.
    """
    def __init__(self, root, volver_callback):
        """
        Inicializa la interfaz y sus componentes principales.
        """
        self.root = root
        self.volver_callback = volver_callback
        self.current_frame = None
        self.browser_process = None
        self.cerrar_btn = None
        self.browser_bar = None

    def mostrar_interfaz_streaming(self):
        """
        Configura y muestra la interfaz gráfica de streaming.
        """
        self.current_frame = tk.Frame(self.root)
        self.current_frame.pack(fill="both", expand=True)

        monitor = get_monitors()[0]
        screen_width = monitor.width
        screen_height = monitor.height

        fondo_img = Image.open("img_interfaz/Fondo.jpg").resize(
            (screen_width, screen_height), Image.Resampling.LANCZOS
        )
        fondo = ImageTk.PhotoImage(fondo_img)
        fondo_label = tk.Label(self.current_frame, image=fondo)
        fondo_label.image = fondo
        fondo_label.place(x=0, y=0, relwidth=1, relheight=1)

        barra_sup = tk.Label(
            self.current_frame,
            bg="#003264",
            fg="white",
            font=("Arial", 24),
            text="Streaming",
        )
        barra_sup.place(x=0, y=0, width=screen_width, height=screen_height // 10)

        volver_btn = tk.Button(
            self.current_frame,
            text="Volver",
            font=("Arial", 12),
            bg="#00FFFF",
            fg="black",
            command=self.volver_callback,
        )
        volver_btn.place(x=10, y=15, width=screen_width // 10, height=screen_height // 20)

        barra_inf = tk.Label(
            self.current_frame,
            text="Marco, Monse & Leo",
            bg="#003264",
            fg="white",
            font=("Arial", 12),
        )
        barra_inf.place(
            x=0,
            y=screen_height - screen_height // 15,
            width=screen_width,
            height=screen_height // 15,
        )

        mensaje_label = tk.Label(
            self.current_frame,
            text="¿Qué quieres ver o escuchar?",
            font=("Arial", 18),
            fg="white",
            bg="#003264",
        )
        mensaje_label.place(x=0, y=screen_height // 10, width=screen_width)

        self.crear_botones_streaming(screen_width, screen_height)

    def crear_botones_streaming(self, screen_width, screen_height):
        """
        Crea los botones con las plataformas de streaming disponibles.
        """
        botones = [
            {"path": "img_interfaz/Netflix.png", "label": "Netflix", "url": "https://www.netflix.com"},
            {"path": "img_interfaz/Prime.png", "label": "Prime", "url": "https://www.primevideo.com"},
            {"path": "img_interfaz/HBOmax.png", "label": "HBO", "url": "https://www.hbomax.com"},
            {"path": "img_interfaz/Disney.png", "label": "Disney", "url": "https://www.disneyplus.com"},
            {"path": "img_interfaz/deezer.png", "label": "Deezer", "url": "https://www.deezer.com"},
            {"path": "img_interfaz/Spotify.png", "label": "Spotify", "url": "https://www.spotify.com"},
        ]

        button_width = screen_width // 8
        button_height = screen_height // 8
        margin_x = screen_width // 30
        margin_y = screen_height // 30

        total_width = 3 * button_width + 2 * margin_x
        total_height = 2 * button_height + margin_y
        x_start = (screen_width - total_width) // 2
        y_start = (screen_height - total_height) // 2

        for i, boton in enumerate(botones):
            img = Image.open(boton["path"]).resize((button_width, button_height), Image.Resampling.LANCZOS)
            boton_img = ImageTk.PhotoImage(img)

            button = tk.Button(
                self.current_frame,
                image=boton_img,
                command=lambda url=boton["url"]: self.abrir_navegador(url),
                borderwidth=0,
                highlightthickness=0,
                relief="flat",
                bg="#003264",
            )
            button.image = boton_img

            x_pos = x_start + (i % 3) * (button_width + margin_x)
            y_pos = y_start + (i // 3) * (button_height + margin_y)
            button.place(x=x_pos, y=y_pos, width=button_width, height=button_height)

    def abrir_navegador(self, url):
        """
        Abre un navegador web para acceder a la plataforma de streaming.
        """
        monitor = get_monitors()[0]
        screen_width = monitor.width
        screen_height = monitor.height

        altura_navegador = screen_height - screen_height // 10
        y_pos = screen_height // 10

        self.browser_process = subprocess.Popen(
            [
                "chromium-browser",
                f"--window-size={screen_width},{altura_navegador}",
                f"--window-position=0,{y_pos}",
                "--disable-extensions",
                "--disable-plugins",
                "--app=" + url,
            ]
        )

        self.browser_bar = tk.Label(
            self.root,
            text="Streaming",
            font=("Arial", 24),
            bg="#003264",
            fg="white",
        )
        self.browser_bar.place(x=0, y=0, width=screen_width, height=screen_height // 10)

        self.cerrar_btn = tk.Button(
            self.root,
            text="Cerrar Navegador",
            font=("Arial", 12),
            bg="red",
            fg="white",
            command=self.forzar_cerrar_navegador,
        )
        self.cerrar_btn.place(x=10, y=10, width=150, height=40)

        self.root.after(1000, self.verificar_navegador)

    def verificar_navegador(self):
        """
        Verifica si el navegador sigue abierto y actualiza los elementos gráficos.
        """
        if self.browser_process and self.browser_process.poll() is None:
            self.root.after(1000, self.verificar_navegador)
        else:
            self.limpiar_elementos()

    def forzar_cerrar_navegador(self):
        """
        Cierra el navegador manualmente.
        """
        if self.browser_process:
            os.kill(self.browser_process.pid, signal.SIGTERM)
            self.browser_process = None
        self.limpiar_elementos()

    def limpiar_elementos(self):
        """
        Elimina los elementos gráficos relacionados con el navegador.
        """
        if self.browser_bar:
            self.browser_bar.destroy()
            self.browser_bar = None

        if self.cerrar_btn:
            self.cerrar_btn.destroy()
            self.cerrar_btn = None

        print("Navegador cerrado y elementos eliminados.")


if __name__ == "__main__":
    def volver_a_menu():
        print("Volviendo al menú principal...")

    root = tk.Tk()
    root.geometry("800x600")
    app = StreamingInterface(root, volver_a_menu)
    app.mostrar_interfaz_streaming()
    root.mainloop()
