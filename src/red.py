import tkinter as tk
from screeninfo import get_monitors
from wifi_manager import WifiManager


class RedInterface:
    """
    Clase para gestionar la configuración de redes WiFi.
    Permite escanear redes, conectarse y mostrar el estado actual de la conexión.
    """
    def __init__(self, root, volver_callback):
        """
        Inicializa la interfaz de red y obtiene el estado inicial de las redes.
        """
        self.root = root
        self.volver_callback = volver_callback
        self.current_frame = None
        self.selected_network = None
        self.networks = []
        self.is_connected = False
        self.wifi_manager = WifiManager()
        self.network_index = 0
        self.obtener_estado_inicial()

    def obtener_estado_inicial(self):
        """
        Obtiene el estado actual de conexión y redes disponibles.
        """
        self.is_connected = self.wifi_manager.is_connected()
        self.networks = self.eliminar_redes_repetidas(self.wifi_manager.scan_networks())

    def eliminar_redes_repetidas(self, networks):
        """
        Elimina redes duplicadas basándose en sus nombres (SSID).
        """
        return sorted(list(set(networks)))

    def mostrar_interfaz_red(self):
        """
        Configura la interfaz gráfica para la gestión de redes.
        """
        self.current_frame = tk.Frame(self.root)
        self.current_frame.pack(fill="both", expand=True)

        monitor = get_monitors()[0]
        screen_width = monitor.width
        screen_height = monitor.height

        fondo_label = tk.Label(self.current_frame, bg="#003264")
        fondo_label.place(x=0, y=0, relwidth=1, relheight=1)

        barra_sup = tk.Label(
            self.current_frame, bg="#003264", fg="white", font=("Arial", 24), text="Configuración de Red"
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

        refresh_btn = tk.Button(
            self.current_frame,
            text="Refrescar",
            font=("Arial", 12),
            bg="#00FFFF",
            fg="black",
            command=self.refrescar_redes,
        )
        refresh_btn.place(x=screen_width - screen_width // 10 - 20, y=15, width=screen_width // 10, height=screen_height // 20)

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

        self.conexion_label = tk.Label(
            self.current_frame,
            text="Conectado" if self.is_connected else "Desconectado",
            bg="#003264",
            fg="green" if self.is_connected else "red",
            font=("Arial", 12),
        )
        self.conexion_label.place(x=screen_width - 200, y=screen_height - 40)

        redes_frame = tk.Frame(self.current_frame, bg="gray")
        frame_width = screen_width // 3
        frame_height = screen_height // 2
        redes_frame.place(x=(screen_width - frame_width) // 2, y=screen_height // 6, width=frame_width, height=frame_height)

        redes_label = tk.Label(
            redes_frame,
            text="Redes disponibles",
            bg="gray",
            fg="white",
            font=("Arial", 16),
        )
        redes_label.pack(pady=10)

        self.redes_list_frame = tk.Frame(redes_frame, bg="gray")
        self.redes_list_frame.pack(fill="both", expand=True)

        self.crear_botones_red(frame_width, frame_height)

        self.config_frame = tk.Frame(self.current_frame, bg="#003264")
        self.config_frame.place(
            x=(screen_width - frame_width) // 2,
            y=screen_height // 6 + frame_height + 20,
            width=frame_width,
            height=screen_height // 5,
        )

        self.password_label = tk.Label(
            self.config_frame, text="Contraseña:", font=("Arial", 14), fg="white", bg="#003264"
        )
        self.password_label.place(x=20, y=20)

        self.password_entry = tk.Entry(
            self.config_frame, font=("Arial", 14), show="*", state="disabled"
        )
        self.password_entry.place(x=20, y=60, width=frame_width - 40)

        self.enviar_button = tk.Button(
            self.config_frame,
            text="Enviar",
            font=("Arial", 14),
            bg="#00FFFF",
            fg="black",
            state="disabled",
            command=self.enviar_datos,
        )
        self.enviar_button.place(x=frame_width // 3, y=120, width=120, height=40)

    def crear_botones_red(self, frame_width, frame_height):
        """
        Crea botones para cada red disponible y controla la navegación.
        """
        for widget in self.redes_list_frame.winfo_children():
            widget.destroy()

        button_height = frame_height // 9
        redes_mostradas = self.networks[self.network_index: self.network_index + 7]
        for red in redes_mostradas:
            btn = tk.Button(
                self.redes_list_frame,
                text=red,
                font=("Arial", 12),
                bg="#00FFFF",
                fg="black",
                command=lambda r=red: self.seleccionar_red(r),
            )
            btn.pack(fill="x", pady=5, padx=10)

        navigation_frame = tk.Frame(self.redes_list_frame, bg="gray")
        navigation_frame.pack(side="bottom", pady=5)

        up_btn = tk.Button(
            navigation_frame,
            text="↑",
            font=("Arial", 14),
            bg="#00FFFF",
            fg="black",
            command=self.subir_redes,
        )
        up_btn.pack(side="left", padx=5)
        if self.network_index == 0:
            up_btn.config(state="disabled")

        down_btn = tk.Button(
            navigation_frame,
            text="↓",
            font=("Arial", 14),
            bg="#00FFFF",
            fg="black",
            command=self.bajar_redes,
        )
        down_btn.pack(side="right", padx=5)
        if self.network_index + 7 >= len(self.networks):
            down_btn.config(state="disabled")

    def subir_redes(self):
        """
        Desplaza hacia arriba la lista de redes disponibles.
        """
        if self.network_index > 0:
            self.network_index -= 7
            self.crear_botones_red(self.redes_list_frame.winfo_width(), self.redes_list_frame.winfo_height())

    def bajar_redes(self):
        """
        Desplaza hacia abajo la lista de redes disponibles.
        """
        if self.network_index + 7 < len(self.networks):
            self.network_index += 7
            self.crear_botones_red(self.redes_list_frame.winfo_width(), self.redes_list_frame.winfo_height())

    def seleccionar_red(self, red):
        """
        Selecciona una red WiFi y habilita la entrada de contraseña.
        """
        if self.selected_network == red:
            self.selected_network = None
            self.password_entry.delete(0, tk.END)
            self.password_entry.config(state="disabled")
            self.enviar_button.config(state="disabled")
        else:
            self.selected_network = red
            self.password_entry.config(state="normal")
            self.enviar_button.config(state="normal")

    def enviar_datos(self):
        """
        Conecta a la red seleccionada usando WifiManager.
        """
        if self.selected_network is not None:
            network = self.selected_network
            password = self.password_entry.get()
            conexion_exitosa = self.wifi_manager.connect_to_network(network, password)
            if conexion_exitosa:
                self.actualizar_estado_conexion()
                print(f"Conexión exitosa a: {network}")
            else:
                self.actualizar_estado_conexion()
                print(f"Error al conectar a: {network}")
            self.password_entry.delete(0, tk.END)
            self.password_entry.config(state="disabled")
            self.enviar_button.config(state="disabled")
        else:
            print("Error: Selecciona una red para continuar.")

    def actualizar_estado_conexion(self):
        """
        Actualiza el estado de conexión en la interfaz.
        """
        if self.wifi_manager.is_connected():
            self.conexion_label.config(text="Conectado", fg="green")
        else:
            self.conexion_label.config(text="Desconectado", fg="red")

    def refrescar_redes(self):
        """
        Escanea y actualiza la lista de redes disponibles.
        """
        self.networks = self.eliminar_redes_repetidas(self.wifi_manager.scan_networks())
        self.network_index = 0
        self.crear_botones_red(self.redes_list_frame.winfo_width(), self.redes_list_frame.winfo_height())
