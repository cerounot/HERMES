import os
import json
import pyaudio
import unicodedata
from vosk import Model, KaldiRecognizer
from PIL import Image, ImageTk
import tkinter as tk
import time

# Ruta al modelo de Idioma descargado.
modelo_idioma = "vosk-model-small-es-0.42"

# Inicializar el modelo de Vosk
if not os.path.exists(modelo_idioma):
    print(f"El modelo en {modelo_idioma} no se encuentra")
    exit()

model = Model(modelo_idioma)
rec = KaldiRecognizer(model, 16000)

# Queue
queue_imgs = []
is_on_queue = False

def normalize_str(texto):
    return ''.join(c for c in unicodedata.normalize('NFKD', texto) if unicodedata.category(c) != 'Mn')

def showImgs():
    global is_on_queue, queue_imgs
    print("######### Probando Queue #########")
    is_on_queue = True
    open_window()
    queue_imgs.clear()
    is_on_queue = False
    print("######### Fin de la Prueba de Queue #########")

def update_image_label(image_path):
    # Abrimos la imagen con Pillow y luego le cambiamos el tamaño
    img = Image.open(image_path)
    img = img.resize((root.winfo_screenwidth(), root.winfo_screenheight()))
    img_tk = ImageTk.PhotoImage(img)
    image_label.config(image=img_tk)
    image_label.image = img_tk

def cycle_images():
    for img_name in queue_imgs:
        img_name_cleaned = normalize_str(img_name)  # Limpiar el nombre del archivo
        img_path = os.path.join("img", img_name_cleaned + ".png")
        try:
            update_image_label(img_path)
            root.update()  # Actualiza la interfaz
            time.sleep(0.5)  # Espera 0.5 segundos antes de mostrar la siguiente imagen
        except Exception as e:
            print(f"Error al mostrar la imagen {img_name}: {e}")
    root.after(500, root.destroy)  # Cierra la ventana después de 0.5 segundos de mostrar la última imagen

def open_window():
    global root, image_label

    # Crear la ventana principal
    root = tk.Tk()
    root.attributes('-fullscreen', True)  # Iniciar en pantalla completa
    root.title("DEBUGGER")

    # Crear un recuadro para mostrar imágenes
    image_label = tk.Label(root)
    image_label.pack()

    # Iniciar el ciclo de imágenes
    cycle_images()

    # Ejecutar la aplicación
    root.mainloop()

# Instanciar PyAudio y crear un Objeto Stream
pAudio = pyaudio.PyAudio()
try:
    stream = pAudio.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8192)
    stream.start_stream()
    print("Por favor, hable ahora...")
    # Capturar el audio en bucle y procesarlo
    while True:
        try:
            data = stream.read(4096, exception_on_overflow=False)
            if rec.AcceptWaveform(data):
                resultObj = json.loads(rec.Result())
                transcripcion = resultObj.get("text", "")
                if transcripcion:
                    if is_on_queue is False:
                        print(f"Dijiste: {transcripcion}")
                        # Separar las palabras en letras individuales
                        letras = list(transcripcion)
                        # Añadir las letras a la queue de imágenes
                        queue_imgs.extend(letras)
                        # Mostrar las imágenes
                        showImgs()
                else:
                    pass
        except KeyboardInterrupt:
            print("Interrupción recibida, deteniendo...")
            break
        except Exception as e:
            print(f"Error al procesar el audio: {e}")
            break
finally:
    # Parar y cerrar el Stream
    stream.stop_stream()
    stream.close()
    pAudio.terminate()
    print("Stream terminado correctamente.")
