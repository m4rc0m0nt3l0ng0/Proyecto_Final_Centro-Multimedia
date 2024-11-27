# Centro Multimedia para Raspberry Pi

Este proyecto implementa un Centro Multimedia basado en Python que permite gestionar diferentes tipos de contenido (audio, video, imágenes) desde dispositivos USB, redes WiFi y plataformas de streaming. La aplicación está diseñada para ejecutarse en una Raspberry Pi con un entorno gráfico basado en `Tkinter`.

## Contenido del Proyecto

### 1. **main.py**
La entrada principal del programa. Contiene la clase `CentroMultimedia`, que gestiona el menú principal del sistema y permite la navegación a las diferentes interfaces (USB, Red y Streaming).

### 2. **usb.py**
Gestiona los dispositivos USB conectados. Permite detectar archivos multimedia, clasificarlos (imágenes, música, videos) y realizar acciones específicas como ver presentaciones, escuchar música o reproducir videos.

### 3. **audio_usb.py**
Permite la reproducción de archivos de audio desde dispositivos USB. Implementa la clase `AudioUSB`, que utiliza `vlc` para la reproducción de música y un temporizador para manejar la reproducción automática.

### 4. **video_usb.py**
Administra la reproducción de videos desde dispositivos USB. Incluye la clase `VideoUSB`, que permite la reproducción individual o en secuencia (presentación de videos) utilizando la biblioteca `vlc`.

### 5. **image_slideshow.py**
Muestra presentaciones de imágenes desde dispositivos USB. La clase `ImageSlideshow` permite navegar por las imágenes automáticamente con un intervalo predefinido.

### 6. **red.py**
Gestiona la conexión a redes WiFi. La clase `RedInterface` permite escanear redes disponibles, conectarse a una red mediante una contraseña y mostrar el estado de conexión actual.

### 7. **streaming.py**
Proporciona acceso a plataformas de streaming como Netflix, Prime Video, HBO Max, Disney+, Spotify y Deezer. La clase `StreamingInterface` abre las plataformas en un navegador Chromium configurado para pantalla completa.

### 8. **wifi_manager.py**
Una clase auxiliar para gestionar redes WiFi mediante comandos `nmcli`. Incluye funciones para verificar si hay conexión, escanear redes disponibles y conectarse a una red específica.

### 9. **media_manager.py**
Permite la detección y clasificación de archivos multimedia (imágenes, música, videos) desde dispositivos USB. También implementa la funcionalidad para montar automáticamente dispositivos USB utilizando `udisksctl`.

### 10. **start.sh**
Un script para iniciar el programa principal (`main.py`) en un entorno gráfico de Raspberry Pi. Configura el servidor Xorg, el entorno de visualización y ejecuta el programa automáticamente.

## Requisitos

### Software
- Python 3.x
- Bibliotecas Python necesarias (instalables con `pip`):
  - `tkinter`
  - `Pillow`
  - `vlc`
  - `pyudev`
  - `screeninfo`
- `nmcli` para la gestión de redes WiFi.
- `udisksctl` para montar dispositivos USB automáticamente.
- Chromium para las plataformas de streaming.

### Hardware
- Raspberry Pi con soporte para Xorg y un entorno gráfico.
- Conexión WiFi y acceso a dispositivos USB.
