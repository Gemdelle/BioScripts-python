from PIL import Image, ImageTk
import tkinter as tk

class AnimatedGIF(tk.Label):
    def __init__(self, canvas, path, x, y):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.path = path
        self.gif = Image.open(path)
        self.frames = []
        self.times = []
        try:
            while True:
                self.frames.append(self.gif.copy())
                self.times.append(self.gif.info['duration'])
                self.gif.seek(len(self.frames))
        except EOFError:
            pass
        self.index = 0
        self.gif = None
        self.delay = sum(self.times)
        self.update_animation()

    def update_animation(self):
        self.index += 1
        if self.index >= len(self.frames):
            self.index = 0
        self.gif = ImageTk.PhotoImage(self.frames[self.index])
        self.canvas.create_image(self.x, self.y, anchor=tk.NW, image=self.gif)
        self.canvas.after(self.times[self.index], self.update_animation)