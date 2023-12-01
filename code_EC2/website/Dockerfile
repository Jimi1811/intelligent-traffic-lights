# Utiliza una imagen base de Ubuntu
FROM ubuntu

# Etiqueta del mantenedor
LABEL maintainer jim.fabian@utec.edu.pe

# Actualiza la lista de paquetes e instala Python 3, pip y git
RUN apt-get update && apt-get install -y python3 python3-pip git

# Establece el directorio de trabajo
WORKDIR /home/ubuntu/intelligent-traffic-lights/code_EC2website

COPY requirements.txt /website
RUN pip3 install -r requirements.txt

# Expone el puerto 5000 para la aplicación Flask (ajusta según tus necesidades)
EXPOSE 5000

# Comando para ejecutar la aplicación Flask
CMD ["/bin/bash", "-c", "python3 src/app.py"]