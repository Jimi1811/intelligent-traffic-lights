#################################################################
##################### Importar librerias ########################
#################################################################

from app import app, socketio

#################################################################
##################### Ejecucion #################################
#################################################################

if __name__ == '__main__':
    camera.start_preview()  # Iniciar vista previa de la cámara
    socketio.start_background_task(target=generate_stream)
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)

