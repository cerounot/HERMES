import os
from PIL import Image
import unicodedata

def normalize_str(texto):
    return ''.join(c for c in unicodedata.normalize('NFKD', texto) if unicodedata.category(c) != 'Mn')

class QueueProcessor:
    def __init__(self):
        self.queue = []
        self.queue_imgs = []
        self.is_on_queue = False

    def isOnQueue(self):
        return self.is_on_queue
    
    def setOnQueue(self, isOn):
        self.is_on_queue = isOn

    def getImgsQueue(self):
        return self.queue_imgs

    def add_transcription(self, transcription):
        self.queue_imgs.extend(transcription)
        self.queue.extend(transcription.split(' '))

    def process_queue(self):
        self.show_imgs()
        self.translate()

    def translate(self):
        print("######### Probando Queue #########")
        self.is_on_queue = True
        for x in self.queue:
            if len(x) > 1:
                print("Imagen")
            else:
                print("Letra")
        self.queue.clear()
        self.is_on_queue = False
        print("######### Fin de la Prueba de Queue #########")

    def show_imgs(self):
        print("######### Probando Queue #########")
        self.is_on_queue = True
        for img_name in self.queue_imgs:
            img_name_cleaned = normalize_str(img_name)
            img_path = os.path.join("img", img_name_cleaned + ".png")
            try:
                img = Image.open(img_path)
                img.show()
            except Exception as e:
                print(f"Error al mostrar la imagen {img_name}: {e}")
        self.queue_imgs.clear()
        self.queue.clear()
        self.is_on_queue = False
        print("######### Fin de la Prueba de Queue #########")