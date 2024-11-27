import subprocess
import socket

class WifiManager:
    """
    Clase para gestionar la conexión a redes WiFi.
    Proporciona funciones para verificar la conexión, escanear redes y conectarse.
    """

    def is_connected(self):
        """
        Verifica si hay una conexión activa a internet.
        """
        try:
            socket.create_connection(("8.8.8.8", 53), timeout=2)
            return True
        except OSError:
            return False

    def scan_networks(self):
        """
        Escanea las redes WiFi disponibles y devuelve sus SSIDs.
        """
        try:
            result = subprocess.run(
                ["nmcli", "-t", "-f", "SSID", "dev", "wifi", "list", "ifname", "wlan0"],
                capture_output=True,
                text=True
            )
            if result.returncode != 0:
                return []
            networks = [ssid.strip() for ssid in result.stdout.split('\n') if ssid.strip()]
            return networks
        except Exception:
            return []

    def connect_to_network(self, ssid, password):
        """
        Intenta conectarse a una red WiFi usando el SSID y contraseña proporcionados.
        """
        try:
            connection_result = subprocess.run(
                ["nmcli", "dev", "wifi", "connect", ssid, "password", password, "ifname", "wlan0"],
                capture_output=True,
                text=True
            )
            return connection_result.returncode == 0
        except Exception:
            return False
