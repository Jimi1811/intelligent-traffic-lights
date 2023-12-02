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

# Requisitos del sistema
## Página web 
