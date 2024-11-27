#!/bin/bash

# Verifica si el script se está ejecutando como superusuario.
if [ "$EUID" -ne 0 ]; then
  echo "Reiniciando el script como superusuario..."
  sudo su -c "/bin/bash $0"  # Reinicia el script con permisos de superusuario.
  exit  # Termina la ejecución del script actual.
fi

# Define el nombre del servicio relacionado con el servidor gráfico Xorg.
SERVICE_NAME="xorg.service"

# Detiene el servicio Xorg si está activo.
echo "Deteniendo el servicio $SERVICE_NAME..."
if systemctl is-active --quiet $SERVICE_NAME; then
  sudo systemctl stop $SERVICE_NAME  # Detiene el servicio.
  echo "Servicio $SERVICE_NAME detenido correctamente."
else
  echo "El servicio $SERVICE_NAME no estaba corriendo."
fi

# Inicia el servicio Xorg nuevamente.
echo "Iniciando el servicio $SERVICE_NAME..."
sudo systemctl start $SERVICE_NAME

# Verifica si el servicio se inició correctamente.
if systemctl is-active --quiet $SERVICE_NAME; then
  echo "Servicio $SERVICE_NAME iniciado correctamente."
else
  echo "Error: No se pudo iniciar el servicio $SERVICE_NAME."
  exit 1  # Sale del script con código de error.
fi

# Verifica si el servidor Xorg está activo.
echo "Verificando si Xorg está corriendo..."
if ! pgrep Xorg > /dev/null; then
  echo "Iniciando Xorg..."
  startx &  # Inicia el entorno gráfico.
  sleep 5  # Espera unos segundos para asegurar que Xorg se inicie correctamente.
fi

# Configura la variable de entorno DISPLAY para el servidor gráfico.
export DISPLAY=:0

# Ejecuta el programa Python principal.
echo "Iniciando programa Python..."
python3 /home/pi/main.py
