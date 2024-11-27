import tkinter as tk
from PIL import Image, ImageTk
from screeninfo import get_monitors

class ImageSlideshow:
    """
    Clase para gestionar una presentación de imágenes en pantalla completa.
    Permite cambiar imágenes automáticamente y regresar a una interfaz previa.
    """
    def __init__(self, root, image_paths, volver_callback):
        """
        Inicializa los parámetros de la presentación, como las rutas de imágenes y el callback.
        """
        self.root = root
        self.image_paths = image_paths
        self.volver_callback = volver_callback
        self.current_frame = None
        self.current_image_index = 0
        self.slideshow_running = True

        monitor = get_monitors()[0]
        self.screen_width = monitor.width
        self.screen_height = monitor.height

    def mostrar_presentacion(self):
        """
        Configura la interfaz gráfica para mostrar las imágenes en secuencia.
        """
        if self.current_frame:
            self.current_frame.destroy()

        self.current_frame = tk.Frame(self.root, bg="black")
        self.current_frame.pack(fill="both", expand=True)

        self.image_label = tk.Label(self.current_frame, bg="black")
        self.image_label.pack(fill="both", expand=True)

        volver_btn = tk.Button(
            self.current_frame,
            text="Regresar",
            font=("Arial", 14),
            bg="#00FFFF",
            fg="black",
            command=self.volver
        )
        volver_btn.place(relx=0.9, rely=0.9, anchor="center")

        self.cambiar_imagen()

    def cambiar_imagen(self):
        """
        Cambia la imagen mostrada de forma cíclica cada 5 segundos.
        """
        if self.slideshow_running and self.image_paths:
            image_path = self.image_paths[self.current_image_index]
            img = Image.open(image_path).resize(
                (self.screen_width, self.screen_height), Image.Resampling.LANCZOS
            )
            img_tk = ImageTk.PhotoImage(img)
            self.image_label.config(image=img_tk)
            self.image_label.image = img_tk

            self.current_image_index = (self.current_image_index + 1) % len(self.image_paths)
            self.root.after(5000, self.cambiar_imagen)

    def volver(self):
        """
        Detiene la presentación y regresa a la interfaz anterior mediante el callback.
        """
        self.slideshow_running = False
        self.current_frame.destroy()
        self.volver_callback()


# Código para probar la clase
if __name__ == "__main__":
    def volver_a_menu():
        print("Regresando al menú principal...")

    image_paths = ["img1.jpg", "img2.jpg", "img3.jpg"]

    root = tk.Tk()
    slideshow = ImageSlideshow(root, image_paths, volver_a_menu)

    monitor = get_monitors()[0]
    root.geometry(f"{monitor.width}x{monitor.height}")
    root.title("Presentación de Imágenes")

    slideshow.mostrar_presentacion()
    root.mainloop()
