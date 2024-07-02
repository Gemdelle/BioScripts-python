import subprocess
import tkinter as tk
from tkinter import scrolledtext

from PIL import Image, ImageTk

from utils.constants import Constants
from utils.resource_path_util import resource_path
from utils.set_time_out_manager import SetTimeoutManager

class FatherGame:
    def __init__(self, root, go_next):
        self.objects = {}
        self.move_commands = {
                    "MoveEast": lambda: self.move_right(self.objects['father']),
                    "MoveWest": lambda: self.move_left(self.objects['father']),
                    "MoveNorth": lambda: self.move_up(self.objects['father']),
                    "MoveSouth": lambda: self.move_down(self.objects['father'])
                }
        self.map_limit_x = 4
        self.map_limit_y = 4
        self.has_lost = False
        self.has_win = False
        self.setTimeoutManager = SetTimeoutManager()
        self.root = root
        self.go_next = go_next
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()

        self.canvas = tk.Canvas(self.root)
        self.canvas.pack(fill=tk.BOTH, expand=tk.YES)

        bg_image = Image.open(resource_path("assets\\images\\coding-background.png"))
        bg_image = bg_image.resize((screen_width, screen_height))
        bg_image_tk = ImageTk.PhotoImage(bg_image)
        setattr(self.canvas, f"bg_image_tk", bg_image_tk)
        self.canvas.create_image(0, 0, anchor='nw', image=bg_image_tk, tags="bg_image")

        # Load and display image
        code_image_container = Image.open(resource_path("assets\\images\\coding-area.png"))
        code_image_container_tk = ImageTk.PhotoImage(code_image_container)
        setattr(self.canvas, f"code_image_container_tk", code_image_container_tk)
        self.canvas.create_image(10, 10, anchor='nw', image=code_image_container_tk, tags="code_image_container")

        # Input text area
        self.input_text = scrolledtext.ScrolledText(self.root, width=50, height=30, bg='#fefbe6', borderwidth=0, highlightthickness=0, wrap=tk.NONE)
        self.input_text.insert(tk.END, Constants.INITIAL_FATHER_GAME_TEXT)
        self.input_text.config(xscrollcommand=None, yscrollcommand=None)  # Disable both horizontal and vertical scrollbars
        self.canvas.create_window(200, 220, anchor='nw', window=self.input_text)

        # Bind arrow key events to manually scroll the text
        self.input_text.bind("<Up>", self.scroll_text)
        self.input_text.bind("<Down>", self.scroll_text)

        # Load run button image
        run_button_image = Image.open(resource_path("assets\\images\\heart-dead.png"))
        run_button_image = run_button_image.resize((100, 40))
        self.run_button_image_tk = ImageTk.PhotoImage(run_button_image)

        # Create a clickable image
        self.run_button = tk.Label(self.root, image=self.run_button_image_tk, borderwidth=0)
        self.run_button.bind("<Button-1>", self.run_java_code)  # Bind left mouse button click
        self.canvas.create_window(300, 800, anchor='nw', window=self.run_button)

        # Output text area
        self.output_text = scrolledtext.ScrolledText(self.root, width=44, height=6, bg='#fefbe6', borderwidth=0, highlightthickness=0, wrap=tk.NONE)
        self.canvas.create_window(210, 875, anchor='nw', window=self.output_text)

        # TileMap related
        self.tile_size = 170
        self.grid_size = 5
        tile_map_offset = 150
        self.tile_map = tk.Canvas(self.canvas, width=self.tile_size * self.grid_size, height=self.tile_size * self.grid_size, borderwidth=0, highlightthickness=0)
        self.create_objects()
        self.canvas.create_window(screen_width - (self.tile_size * self.grid_size) - tile_map_offset, screen_height - (self.tile_size * self.grid_size) - tile_map_offset, anchor='nw', window=self.tile_map)
        mini_game_map_image = Image.open(resource_path("assets\\images\\mini-game-map.png"))
        mini_game_map_image = mini_game_map_image.resize((850, 850))
        mini_game_map_image_tk = ImageTk.PhotoImage(mini_game_map_image)
        setattr(self.tile_map, "mini_game_map_image_tk", mini_game_map_image_tk)
        self.tile_map.create_image(0, 0, anchor='nw', image=mini_game_map_image_tk, tags="mini_game_map")

        #self.draw_grid()

        self.objects['father'] = self.tile_map.create_oval(
            self.get_centered_coords(0, 4, offset=self.tile_size // 4), fill='white')

    def draw_grid(self):
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                x1 = j * self.tile_size
                y1 = i * self.tile_size
                x2 = x1 + self.tile_size
                y2 = y1 + self.tile_size
                self.tile_map.create_rectangle(x1, y1, x2, y2, outline='black')

    def create_objects(self):
        self.objects['crystal1'] = self.tile_map.create_oval(
            self.get_centered_coords(1, 1, offset=self.tile_size // 4), fill='orange')
        self.objects['crystal2'] = self.tile_map.create_oval(
            self.get_centered_coords(2, 3, offset=self.tile_size // 4), fill='grey')
        self.objects['crystal3'] = self.tile_map.create_oval(
            self.get_centered_coords(3, 1, offset=self.tile_size // 4), fill='red')
        self.objects['crystal4'] = self.tile_map.create_oval(
            self.get_centered_coords(1, 4, offset=self.tile_size // 4), fill='blue')
        self.objects['crystal5'] = self.tile_map.create_oval(
            self.get_centered_coords(4, 3, offset=self.tile_size // 4), fill='purple')
        self.objects['food'] = self.tile_map.create_oval(
            self.get_centered_coords(3, 0, offset=self.tile_size // 4), fill='black')


    def get_centered_coords(self, x, y, offset):
        x1 = x * self.tile_size + offset
        y1 = y * self.tile_size + offset
        x2 = x1 + self.tile_size - 2 * offset
        y2 = y1 + self.tile_size - 2 * offset
        return x1, y1, x2, y2

    def move_right(self, obj_id):
        if not self.has_lost:
            self.tile_map.move(obj_id, self.tile_size, 0)
            self.check_if_lost()

    def move_left(self, obj_id):
        if not self.has_lost:
            self.tile_map.move(obj_id, -self.tile_size, 0)
            self.check_if_lost()

    def move_up(self, obj_id):
        if not self.has_lost:
            self.tile_map.move(obj_id, 0, -self.tile_size)
            self.check_if_lost()

    def move_down(self, obj_id):
        if not self.has_lost:
            self.tile_map.move(obj_id, 0, self.tile_size)
            self.check_if_lost()

    def check_if_lost(self):
        father_coords = self.find_object_position_by_id(self.objects['father'])
        for key, value in self.objects.items():
            if self.objects['father'] != value:
                if self.objects['food'] == value:
                    self.has_win = True
                else:
                    value_coords = self.find_object_position_by_id(value)
                    if father_coords[0] == value_coords[0] and father_coords[1] == value_coords[1]:
                        self.has_lost = True
                        self.has_win = False
                    elif not (0 <= father_coords[0] <= self.map_limit_x * self.tile_size) or not (0 <= father_coords[1] <= self.map_limit_y * self.tile_size):
                        self.has_lost = True
                        self.has_win = False

    def find_object_position_by_id(self, obj_id):
        try:
            obj_coords = self.tile_map.coords(obj_id)
            if len(obj_coords) >= 2:
                x, y = obj_coords[0], obj_coords[1]
                return x, y
            else:
                return None
        except tk.TclError:
            return None

    def scroll_text(self, event):
        if event.keysym == "Up":
            self.input_text.yview_scroll(-1, "units")
        elif event.keysym == "Down":
            self.input_text.yview_scroll(1, "units")


    def get_input_text(self):
        return self.input_text.get("1.0", tk.END)

    def run_java_code(self, event):
        java_code = self.get_input_text()

        # Split the Java code into individual class definitions based on "//---"
        java_classes = self.split_java_classes(java_code)

        compile_processes = []

        for java_class in java_classes:
            if java_class.strip().startswith("public class"):
                # Extract class name
                class_name = self.extract_class_name(java_class)

                # Write the Java file
                with open(f"./validations/father_game/{class_name}.java", "w") as file:
                    file.write(java_class)

                # Compile the Java file
                compile_process = subprocess.Popen(["javac", f"{class_name}.java"], stdout=subprocess.PIPE,
                                                   stderr=subprocess.PIPE, cwd="./validations/father_game")
                compile_processes.append((class_name, compile_process))

        try:
            # Wait for all compilation processes to finish
            for class_name, compile_process in compile_processes:
                compile_process.wait(timeout=15)

                # Check compilation result
                if compile_process.returncode != 0:
                    self.output_text.insert(tk.END, f"Compilation Error for {class_name}.java:\n{compile_process.stderr.read().decode()}\n")
                    return

            # If compilation successful, execute the main method of Main class if exists
            main_process = subprocess.Popen(
                ["java", "Main"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                cwd="./validations/father_game"
            )
            main_process.wait(timeout=15)

            # Display output of main execution
            if main_process.returncode == 0:
                output = main_process.stdout.read().decode()
                self.output_text.delete("1.0", tk.END)
                self.output_text.insert(tk.END, output)

                commands = output.split("\r\n")
                current_delay = 1
                for command in commands:
                    command = command.strip()
                    if command in self.move_commands and command != "":
                        self.setTimeoutManager.setTimeout(lambda cmd=command: self.move_commands[cmd](), current_delay)
                        current_delay += 1

                    if command == commands[-1]:
                        self.setTimeoutManager.setTimeout(lambda: self.check_reset_positions(), current_delay+1)
            else:
                self.output_text.delete("1.0", tk.END)
                self.output_text.insert(tk.END, "Error occurred during execution.\n")
                self.output_text.insert(tk.END, main_process.stderr.read().decode())

        except subprocess.TimeoutExpired:
            self.output_text.delete("1.0", tk.END)
            self.output_text.insert(tk.END, "Timeout occurred during compilation or execution.\n")
    def close_game(self):
        self.go_next()

    def check_reset_positions(self):
        if self.has_win:
            self.close_game()
        elif self.has_lost:
            self.move_to_initial_positions()
            self.has_lost = False
            self.has_win = False

    def move_to_initial_positions(self):
        for obj_id in self.objects.values():
            self.tile_map.coords(obj_id, *self.get_initial_position(obj_id))

    def get_initial_position(self, obj_id):
        if obj_id == self.objects['crystal1']:
            return self.get_centered_coords(1, 1, offset=self.tile_size // 4)
        elif obj_id == self.objects['crystal2']:
            return self.get_centered_coords(2, 3, offset=self.tile_size // 4)
        elif obj_id == self.objects['crystal3']:
            return self.get_centered_coords(3, 1, offset=self.tile_size // 4)
        elif obj_id == self.objects['crystal4']:
            return self.get_centered_coords(1, 4, offset=self.tile_size // 4)
        elif obj_id == self.objects['crystal5']:
            return self.get_centered_coords(4, 3, offset=self.tile_size // 4)
        elif obj_id == self.objects['food']:
            return self.get_centered_coords(3, 0, offset=self.tile_size // 4)
        elif obj_id == self.objects['father']:
            return self.get_centered_coords(0, 4, offset=self.tile_size // 4)
        else:
            return (0, 0, 0, 0)


    def split_java_classes(self, java_code):
        java_classes = []
        current_class = ""

        for line in java_code.splitlines():
            if line.strip() == "//---":  # Class limiter
                if current_class.strip():
                    java_classes.append(current_class.strip() + "\n")
                    current_class = ""
            else:
                current_class += line + "\n"

        if current_class.strip():
            java_classes.append(current_class.strip() + "\n")

        return java_classes

    def extract_class_name(self, java_class):
        class_name_start = java_class.index("public class") + len("public class")
        class_name_end = java_class.index("{", class_name_start)
        class_name = java_class[class_name_start:class_name_end].strip()
        return class_name
