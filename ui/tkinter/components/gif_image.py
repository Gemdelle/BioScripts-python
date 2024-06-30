from PIL import Image, ImageTk
import tkinter as tk

class AnimatedGIF:
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
        self.is_running = False  # Flag to track if animation is running
        self.image_id = None
        self.update_animation()

    def update_animation(self):
        if self.is_running:
            self.index += 1
            if self.index >= len(self.frames):
                self.index = 0
            self.gif = ImageTk.PhotoImage(self.frames[self.index])
            if self.image_id is None:
                self.image_id = self.canvas.create_image(self.x, self.y, anchor=tk.NW, image=self.gif)
            else:
                self.canvas.itemconfig(self.image_id, image=self.gif)
            self.canvas.after(self.times[self.index], self.update_animation)

    def start_animation(self):
        self.is_running = True
        self.update_animation()

    def stop_animation(self):
        self.is_running = False

    def destroy(self):
        self.stop_animation()  # Stop the animation if it's running
        if self.image_id is not None:
            self.canvas.delete(self.image_id)  # Remove the image from the canvas
            self.image_id = None

