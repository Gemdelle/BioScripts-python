import tkinter as tk
from PIL import Image, ImageTk


class ClickableImage(tk.Label):
    def __init__(self, master=None, flip=False, **kw):
        self.callback = kw.pop('callback', None)
        self.image_path = kw.pop('image_path', None)
        self.image_size = kw.pop('image_size', (200, 200))
        self.image = self.load_and_resize_image(self.image_path, self.image_size)
        self.photo = ImageTk.PhotoImage(self.image)
        super().__init__(master, image=self.photo, **kw)
        self.bind("<Button-1>", self.on_click)

    def load_and_resize_image(self, image_path, size):
        original_image = Image.open(image_path)
        resized_image = original_image.resize(size)
        return resized_image

    def on_click(self, event):
        if self.callback:
            self.callback()