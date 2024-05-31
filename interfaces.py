import tkinter as tk
import queue_processor as Queue
import os

class Interfaces:
    def __init__(self):
        # Crear la ventana principal
        self.root = tk.Tk()
        self.root.attributes('-fullscreen', True)  # Iniciar en pantalla completa
        self.root.title("DEBUGGER")
        # Crear un recuadro para mostrar imágenes
        image_label = tk.Label(self.root)
        image_label.pack()
        # Iniciar el ciclo de imágenes
        self.cycle_images()
        # Ejecutar la aplicación
        self.root.mainloop()

    def cycle_images(self):
        queue = Queue()
        for img_name in queue.getImgsQueue():
            img_name_cleaned = self.normalize_str(img_name)  # Limpiar el nombre del archivo
            img_path = os.path.join("img", img_name_cleaned + ".png")
            try:
                self.update_image_label(img_path)
                self.root.update()  # Actualiza la interfaz
                self.time.sleep(0.5)  # Espera 0.5 segundos antes de mostrar la siguiente imagen
            except Exception as e:
                print(f"Error al mostrar la imagen {img_name}: {e}")
        self.root.after(200, self.root.destroy)  # Cierra la ventana después de 0.5 segundos de mostrar la última imagen