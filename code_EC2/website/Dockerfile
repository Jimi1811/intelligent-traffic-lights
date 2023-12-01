# Utiliza una imagen base de Ubuntu
FROM ubuntu

# Etiqueta del mantenedor
LABEL maintainer jim.fabian@utec.edu.pe

# Actualiza la lista de paquetes e instala Python 3, pip y git
RUN apt-get update && apt-get install -y python3 python3-pip git

# Clona el repositorio privado utilizando un token de acceso personal (reemplaza 'TU_TOKEN' con tu PAT de GitHub)
RUN git clone https://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@github.com/uteccognitive/2023-2-icc-python-flash-docker-Jimi1811.git /app

# Establece el directorio de trabajo
WORKDIR /website

# Instala las dependencias de la aplicación desde requirements.txt
RUN pip3 install -r requirements.txt

# Expone el puerto 5000 para la aplicación Flask (ajusta según tus necesidades)
EXPOSE 5000

# Comando para ejecutar la aplicación Flask
CMD ["/bin/bash", "-c", "python3 src/app.py"]
