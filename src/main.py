import tkinter as tk
import os
from screeninfo import get_monitors
from PIL import Image, ImageTk
from usb import USBInterface
from streaming import StreamingInterface
from red import RedInterface


class CentroMultimedia:
    """
    Clase principal para gestionar un centro multimedia.
    Permite navegar entre diferentes interfaces: Red, USB y Streaming.
    """
    def __init__(self, root):
        """
        Inicializa el centro multimedia, configurando la ventana principal y el menú.
        """
        self.root = root
        self.root.title("Centro Multimedia")

        monitor = get_monitors()[0]
        self.screen_width = monitor.width
        self.screen_height = monitor.height
        self.root.geometry(f"{self.screen_width}x{self.screen_height}")
        self.root.resizable(True, True)

        self.canvas = None
        self.mostrar_menu_principal()

    def limpiar_ventana(self):
        """
        Elimina todos los elementos actuales de la ventana.
        """
        for widget in self.root.winfo_children():
            widget.destroy()

    def salir_sistema(self):
        """
        Ejecuta un comando para apagar el sistema operativo.
        """
        os.system("shutdown now")

    def mostrar_menu_principal(self):
        """
        Configura y muestra el menú principal con opciones de navegación.
        """
        self.limpiar_ventana()

        fondo_img = Image.open("img_interfaz/Fondo.jpg").resize(
            (self.screen_width, self.screen_height), Image.Resampling.LANCZOS
        )
        fondo = ImageTk.PhotoImage(fondo_img)
        self.canvas = tk.Label(self.root, image=fondo)
        self.canvas.image = fondo
        self.canvas.place(x=0, y=0, relwidth=1, relheight=1)

        barra_sup = tk.Label(
            self.root,
            bg="#003264",
            fg="white",
            font=("Arial", 24),
            text="MML Media Center",
        )
        barra_sup.place(
            x=0,
            y=0,
            width=self.screen_width,
            height=self.screen_height // 10,
        )

        barra_inf = tk.Label(
            self.root,
            text="Marco, Monse & Leo",
            bg="#003264",
            fg="white",
            font=("Arial", 12),
        )
        barra_inf.place(
            x=0,
            y=self.screen_height - self.screen_height // 15,
            width=self.screen_width,
            height=self.screen_height // 15,
        )

        botones = [
            {"text": "Red", "command": self.mostrar_red},
            {"text": "USB", "command": self.mostrar_usb},
            {"text": "Streaming", "command": self.mostrar_streaming},
            {"text": "Salir", "command": self.salir_sistema},
        ]

        button_width = self.screen_width // 8
        button_height = self.screen_height // 15
        start_x = (self.screen_width - (2 * button_width + self.screen_width // 20)) // 2
        start_y = self.screen_height // 3
        margin_x = self.screen_width // 20
        margin_y = self.screen_height // 30

        for i, boton in enumerate(botones):
            x_pos = start_x + (i % 2) * (button_width + margin_x)
            y_pos = start_y + (i // 2) * (button_height + margin_y)
            btn = tk.Button(
                self.root,
                text=boton["text"],
                font=("Arial", 14),
                bg="#00FFFF",
                fg="black",
                command=boton["command"],
            )
            btn.place(x=x_pos, y=y_pos, width=button_width, height=button_height)

    def mostrar_usb(self):
        """
        Cambia a la interfaz de USB.
        """
        usb_interface = USBInterface(self.root, self.mostrar_menu_principal)
        self.limpiar_ventana()
        usb_interface.mostrar_interfaz_usb()

    def mostrar_streaming(self):
        """
        Cambia a la interfaz de Streaming.
        """
        streaming_interface = StreamingInterface(self.root, self.mostrar_menu_principal)
        self.limpiar_ventana()
        streaming_interface.mostrar_interfaz_streaming()

    def mostrar_red(self):
        """
        Cambia a la interfaz de Red.
        """
        red_interface = RedInterface(self.root, self.mostrar_menu_principal)
        self.limpiar_ventana()
        red_interface.mostrar_interfaz_red()


if __name__ == "__main__":
    root = tk.Tk()
    app = CentroMultimedia(root)
    root.mainloop()
