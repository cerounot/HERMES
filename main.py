import time
import tkinter as tk
from PIL import Image, ImageTk
import pyaudio
import numpy as np
import threading
import os
from vosk_recognizer import VoskRecognizer
from queue_processor import QueueProcessor

# Variables globales
is_muted = False
audio_data = np.zeros(1024)
img_dict = {}  # Diccionario para almacenar las imágenes del abecedario

# Inicializar PyAudio
pAudio = pyaudio.PyAudio()

# Función para mutear/desmutear el micrófono
def toggle_mute():
    global is_muted
    is_muted = not is_muted
    btn_mute.config(text="Desmutear" if is_muted else "Mutear")

# Función para cargar las imágenes del abecedario
def cargar_imagenes():
    global img_dict
    for letra in 'abcdefghijklmnopqrstuvwxyz':
        img_path = os.path.join('img', f'{letra}.png')
        if os.path.exists(img_path):
            img = Image.open(img_path)
            img = img.resize((50, 50), Image.LANCZOS)
            img_dict[letra] = ImageTk.PhotoImage(img)

# Función para mostrar las imágenes del abecedario
def mostrar_imagenes(transcripcion):
    for widget in frame_abecedario.winfo_children():
        widget.destroy()
    
    for letra in transcripcion:
        if letra in img_dict:
            lbl_img = tk.Label(frame_abecedario, image=img_dict[letra])
            lbl_img.pack(side=tk.LEFT)

# Función para escuchar y actualizar los datos de audio
def listen_audio():
    global audio_data
    stream = pAudio.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8192)
    stream.start_stream()
    print("Por favor, hable ahora...")

    recognizer = VoskRecognizer("vosk-model-small-es-0.42")
    processor = QueueProcessor()

    # Capturar el audio en bucle y procesarlo
    try:
        while True:
            if not is_muted:
                try:
                    data = stream.read(4096, exception_on_overflow=False)
                    audio_data = np.frombuffer(data, dtype=np.int16)
                    transcription = recognizer.recognize(data)
                    if transcription:
                        print(transcription)
                        if not processor.isOnQueue():  #alexis
                            processor.add_transcription(transcription)
                        mostrar_imagenes(transcription.lower())  # Mostrar las imágenes de la transcripción
                    else:
                        processor.process_queue()
                except KeyboardInterrupt:
                    print("Interrupción recibida, deteniendo...")
                    break
                except Exception as e:
                    print(f"Error al procesar el audio: {e}")
                    break
            else:
                time.sleep(0.1)  # Evitar uso excesivo de CPU
    finally:
        # Parar y cerrar el Stream
        stream.stop_stream()
        stream.close()

# Función para actualizar la gráfica
def update_plot():
    global audio_data
    canvas.delete("all")
    width = canvas.winfo_width()
    height = canvas.winfo_height()
    center = height // 2
    scale = height / 65536
    for i in range(1, len(audio_data)):
        x1 = (i - 1) * width / len(audio_data)
        y1 = center - audio_data[i - 1] * scale
        x2 = i * width / len(audio_data)
        y2 = center - audio_data[i] * scale
        canvas.create_line(x1, y1, x2, y2, fill="blue")
    ventana.after(50, update_plot)

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Interfaz de Visualización de Audio")
ventana.attributes("-fullscreen", True)

# Crear botones para mutear
btn_mute = tk.Button(ventana, text="Mutear", command=toggle_mute)
btn_mute.pack(pady=10)

# Crear un botón para salir de la aplicación
def salir():
    ventana.destroy()

btn_salir = tk.Button(ventana, text="Salir", command=salir)
btn_salir.pack(pady=10)

# Añadir funcionalidad para salir de pantalla completa con ESC
def salir_pantalla_completa(event):
    ventana.attributes("-fullscreen", False)
    ventana.geometry("800x600")

ventana.bind("<Escape>", salir_pantalla_completa)

# Crear un canvas para dibujar la onda sonora
canvas = tk.Canvas(ventana, width=150, height=150)
canvas.pack()

# Crear un frame para mostrar las imágenes del abecedario
frame_abecedario = tk.Frame(ventana)
frame_abecedario.pack()

# Cargar las imágenes del abecedario
cargar_imagenes()

# Iniciar el hilo de escucha de audio
threading.Thread(target=listen_audio, daemon=True).start()

# Iniciar la actualización de la gráfica
ventana.after(10, update_plot)

# Iniciar el bucle principal de la interfaz
ventana.mainloop()

# Parar y cerrar el Stream
pAudio.terminate()
print("Stream terminado correctamente.")
