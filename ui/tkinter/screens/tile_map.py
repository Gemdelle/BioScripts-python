import tkinter as tk


class TileMap(tk.Canvas):
    def __init__(self, parent, tile_size=100, grid_size=5, *args, **kwargs):
        super().__init__(parent, width=tile_size * grid_size, height=tile_size * grid_size, *args, **kwargs)
        self.tile_size = tile_size
        self.grid_size = grid_size
        self.objects = {}

        self.draw_grid()
        self.create_objects()

    def draw_grid(self):
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                x1 = j * self.tile_size
                y1 = i * self.tile_size
                x2 = x1 + self.tile_size
                y2 = y1 + self.tile_size
                self.create_rectangle(x1, y1, x2, y2, outline='black')

    def create_objects(self):
        # Create example objects, centered within the tiles
        self.objects['animal_photo'] = self.create_rectangle(
            self.get_centered_coords(0, 3, offset=self.tile_size // 2), fill='black')
        self.objects['object1'] = self.create_oval(
            self.get_centered_coords(1, 0, offset=self.tile_size // 4), fill='green')
        self.objects['object2'] = self.create_oval(
            self.get_centered_coords(2, 2, offset=self.tile_size // 4), fill='green')
        self.objects['object3'] = self.create_oval(
            self.get_centered_coords(3, 1, offset=self.tile_size // 4), fill='green')
        self.objects['object4'] = self.create_oval(
            self.get_centered_coords(3, 3, offset=self.tile_size // 4), fill='yellow')

    def get_centered_coords(self, x, y, offset):
        x1 = x * self.tile_size + offset
        y1 = y * self.tile_size + offset
        x2 = x1 + self.tile_size - 2 * offset
        y2 = y1 + self.tile_size - 2 * offset
        return x1, y1, x2, y2

    def move_right(self, obj_id):
        self.move(obj_id, self.tile_size, 0)

    def move_left(self, obj_id):
        self.move(obj_id, -self.tile_size, 0)

    def move_up(self, obj_id):
        self.move(obj_id, 0, -self.tile_size)

    def move_down(self, obj_id):
        self.move(obj_id, 0, self.tile_size)

