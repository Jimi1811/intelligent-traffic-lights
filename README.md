# Prototipo de un sistema de semáforos inteligentes

El presente proyecto se embarca en el desarrollo de un sistema de semáforos inteligentes que, a través del reconocimiento de vehículos, estima el nivel de tráfico, proponiendo así una contribución concreta hacia el desarrollo de ciudades más inteligentes y sostenibles. Asimismo, por medio de una página web, se podrá visualizar el estado de los semáforos y video en vivo de la cámara. Aún más, se agrega una base de datos relacional para almacenar las grabaciones de la cámara, así como los estados de los semáforos. A través de estos datos se puede conseguir estadísticas del flujo vehicular.

# Objetivos

## Objetivo general
[] Diseñar e implementar un sistema mecatrónico de semáforos inteligentes junto a una base de datos y página web para una intersección de dos calles usando visión computacional.

## Objetivos específicos

- [x] Diseñar un algoritmo para la detección de vehículos y estinación de tráfico.
- [x] Diseñar un algoritmo para el envío de video en vivo.
- [x] Diseñar un algoritmo para el almacenamiento segmentado de lo enviado en vivo.
- [ ] Integrar los algoritmos mencionados
- [x] Diseñar un algoritmo para la sincronización de las luces de los semáforos.
- [x] Diseñar el entorno de simulación para la aplicación del prototipo.
- [ ] Conectar una página web en EC2 con acceso a la cámara e información del tráfico.
- [ ] Conectar una base de datos MYSQL en EC2 que almacene los estados de los semáforos y grabaciones, y esté conectado a la página web.

# Estructura del proyecto

La estructura del proyecto se divide en 2: 
1. En una instancia de EC2 en AWS se tienen dos contenedores:
  - Página web
      * Flask y MQTT como backend.
      * Template de Bootstrap.
  - Base de datos
      * Base de datos relacional MySQL
      * Creación de 2 tablas:
          * Intersección XX - XX: Información de los cambios de los semáforos
          * Grabaciones: Acceso a las grabaciones de la cámara
2. Raspberry Pi como semáforo:
  - Hardware:
      - Raspberry pi 4B
      - Cámara V3
      - 6 LEDs con resistencia c/u
      - Alimentación

  - Software:
      - Raspberry OS Bookworm
      - Python 3.10
      - Picamera2
      - Tensorflow Lite
      - Flask
      - OpenCV
      - MQTT

# Requisitos del sistema

## Amazon Web Services - EC2
- Ubuntu 22.04
- Docker y Docker Compose
- Python3: 3.10.12
- pip3

## Base de datos
- Raspberry OS Bookworm
- Picamera2

# Instalación

## Página web y base de datos

1. Crea la instancia en AWS con el servicio EC2. Recomendamos que tenga 10 gb de almacenamiento, Ubuntu 22.04.
2. Abrir los siguientes puertos en la sección de seguridad:
   - SSH - TCP - 22 - 0.0.0.0/0
   - Custom TCP - TCP - 4000 - 0.0.0.0/0
   - Custom TCP - TCP - 5000 - 0.0.0.0/0
3. Conéctate a la instancia. Desde tu terminal Linux:
   ```bash
   ssh -i key-<key_server>.pem ubuntu@<Public_IPv4_address>
   ```
5. Una vez conectado, descargar el repositorio:
   ```bash
   git clone https://github.com/Jimi1811/intelligent-traffic-lights.git
   cd intelligent-traffic-lights
   rm -rf code_raspberry code_tests # eliminar codigos innecesarios
   ```
7. Instalar Docker. [Enlace de referencia](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-22-04)
8. Instalar pip3
