import os
import pyudev
from time import sleep
import subprocess as sp

class MediaManager:
    """
    Clase para gestionar archivos multimedia y monitorear dispositivos USB.
    Soporta clasificación de archivos y montado automático.
    """
    def __init__(self):
        """
        Inicializa los formatos de archivo compatibles para imágenes, audio y video.
        """
        self.image_formats = [".jpeg", ".jpg", ".png", ".bmp", ".tiff", ".tif",
                              ".webp", ".tga", ".pam", ".ppm", ".pgm", ".pbm", ".xcf", ".svg"]

        self.audio_formats = [".mp3", ".aac", ".wav", ".flac", ".ogg", ".wma",
                              ".m4a", ".opus", ".aiff", ".amr"]

        self.video_formats = [".mp4", ".avi", ".mkv", ".mov", ".flv", ".webm",
                              ".wmv", ".mpg", ".mpeg", ".m4v", ".3gp", ".ogv",
                              ".divx", ".xvid"]

    def get_media_files(self, path):
        """
        Clasifica archivos en imágenes, audio y video dentro de un directorio dado.
        """
        images = []
        audio_files = []
        video_files = []

        for file in os.listdir(path):
            file_path = os.path.join(path, file)
            if any(file.endswith(ext) for ext in self.image_formats):
                images.append(file_path)
            elif any(file.endswith(ext) for ext in self.audio_formats):
                audio_files.append(file_path)
            elif any(file.endswith(ext) for ext in self.video_formats):
                video_files.append(file_path)

        return images, audio_files, video_files

    def auto_mount(self, path):
        """
        Monta automáticamente un dispositivo en el sistema.
        """
        args = ["udisksctl", "mount", "-b", path]
        sp.run(args)

    def get_mount_point(self, path):
        """
        Obtiene el punto de montaje de un dispositivo dado.
        """
        args = ["findmnt", "-unl", "-S", path]
        cp = sp.run(args, capture_output=True, text=True)
        out = cp.stdout.split(" ")[0]
        return out

    def monitor_devices(self, queue):
        """
        Monitorea dispositivos USB conectados y desconectados, enviando actualizaciones a una cola.
        """
        context = pyudev.Context()
        monitor = pyudev.Monitor.from_netlink(context)
        monitor.filter_by(subsystem="block", device_type="partition")

        for device in iter(monitor.poll, None):
            if device.action == "add":
                try:
                    self.auto_mount("/dev/" + device.sys_name)
                    mount_point = self.get_mount_point("/dev/" + device.sys_name)
                    if mount_point:
                        images, audio_files, video_files = self.get_media_files(mount_point)
                        queue.put(("add", images, audio_files, video_files))
                except Exception as e:
                    print(f"Error al añadir dispositivo: {e}")

            elif device.action == "remove":
                queue.put(("remove", [], [], []))

            sleep(1)
