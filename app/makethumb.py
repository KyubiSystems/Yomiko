from PIL import Image
from io import BytesIO
from os import rename, makedirs, path

class Page(BytesIO):
    def get(self):
        return self.getvalue()

    def img(self):
        return Image.open(BytesIO(self.get()))

    def save(self, path):
        im = self.img()
        im.save(path, 'JPEG')
        return path

    def size(self):
        return self.img().size

    def thumb(self, size=(300, 400)):
        im = self.img()
        im.thumbnail(size, Image.ANTIALIAS)
        self.seek(0)
        im.save(self, 'JPEG')
