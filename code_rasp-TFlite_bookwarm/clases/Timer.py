import time

def timer(duration):
    start_time = time.time() ## inicializa tiempo

    while True:
        elapsed_time = time.time() - start_time ## tiempo transcurrido
        mins, secs = divmod(elapsed_time, 60) ## obtener minutos y segundos
        hours, mins = divmod(mins, 60) ## obtener horas y minutos

        timer_str = "{:02}:{:02}:{:02}".format(int(hours), int(mins), int(secs)) ## tiempo en formato string
        print("\rTiempo transcurrido: {}".format(timer_str), end="") 
        time.sleep(1) 

        if elapsed_time >= duration: ## tiempo de duracion cumplido
            break

    print("\n¡Tiempo transcurrido alcanzado!")

# Duración del temporizador en segundos (por ejemplo, 30 segundo)
duracion_temporizador = 1/2 * 60

# Llamada a la función del temporizador
timer(duracion_temporizador)
