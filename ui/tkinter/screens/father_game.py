import subprocess
import tkinter as tk
from tkinter import scrolledtext

from PIL import Image, ImageTk

from utils.constants import Constants
from utils.resource_path_util import resource_path
from utils.set_time_out_manager import SetTimeoutManager

class FatherGame:
    def __init__(self, root, go_next_validation):
        self.move_commands = {
                    "MoveEast": lambda: self.move_right(self.objects['object4']),
                    "MoveWest": lambda: self.move_left(self.objects['object4']),
                    "MoveNorth": lambda: self.move_up(self.objects['object4']),
                    "MoveSouth": lambda: self.move_down(self.objects['object4'])
                }
        self.setTimeoutManager = SetTimeoutManager()
        self.root = root
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        self.go_next_validation = go_next_validation

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
        self.tile_map = tk.Canvas(self.canvas, width=self.tile_size * self.grid_size, height=self.tile_size * self.grid_size)
        self.canvas.create_window(screen_width - (self.tile_size * self.grid_size) - tile_map_offset, screen_height - (self.tile_size * self.grid_size) - tile_map_offset, anchor='nw', window=self.tile_map)
        self.draw_grid()
        self.create_objects()
        self.setTimeoutManager.setTimeout(lambda: self.move1(), 2)

    def draw_grid(self):
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                x1 = j * self.tile_size
                y1 = i * self.tile_size
                x2 = x1 + self.tile_size
                y2 = y1 + self.tile_size
                self.tile_map.create_rectangle(x1, y1, x2, y2, outline='black')

    def create_objects(self):
        self.objects = {}
        self.objects['animal_photo'] = self.tile_map.create_rectangle(
            self.get_centered_coords(0, 3, offset=self.tile_size // 2), fill='black')
        self.objects['object1'] = self.tile_map.create_oval(
            self.get_centered_coords(1, 0, offset=self.tile_size // 4), fill='green')
        self.objects['object2'] = self.tile_map.create_oval(
            self.get_centered_coords(2, 2, offset=self.tile_size // 4), fill='green')
        self.objects['object3'] = self.tile_map.create_oval(
            self.get_centered_coords(3, 1, offset=self.tile_size // 4), fill='green')
        self.objects['object4'] = self.tile_map.create_oval(
            self.get_centered_coords(3, 3, offset=self.tile_size // 4), fill='yellow')

    def get_centered_coords(self, x, y, offset):
        x1 = x * self.tile_size + offset
        y1 = y * self.tile_size + offset
        x2 = x1 + self.tile_size - 2 * offset
        y2 = y1 + self.tile_size - 2 * offset
        return x1, y1, x2, y2

    def move_right(self, obj_id):
        self.tile_map.move(obj_id, self.tile_size, 0)

    def move_left(self, obj_id):
        self.tile_map.move(obj_id, -self.tile_size, 0)

    def move_up(self, obj_id):
        self.tile_map.move(obj_id, 0, -self.tile_size)

    def move_down(self, obj_id):
        self.tile_map.move(obj_id, 0, self.tile_size)

    def move1(self):
        self.move_left(self.objects['object4'])
        self.setTimeoutManager.setTimeout(lambda: self.move2(), 1)

    def move2(self):
        self.move_down(self.objects['object4'])
        self.setTimeoutManager.setTimeout(lambda: self.move3(), 1)

    def move3(self):
        self.move_left(self.objects['object4'])
        self.setTimeoutManager.setTimeout(lambda: self.move4(), 1)

    def move4(self):
        self.move_up(self.objects['object4'])

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
            else:
                self.output_text.delete("1.0", tk.END)
                self.output_text.insert(tk.END, "Error occurred during execution.\n")
                self.output_text.insert(tk.END, main_process.stderr.read().decode())

        except subprocess.TimeoutExpired:
            self.output_text.delete("1.0", tk.END)
            self.output_text.insert(tk.END, "Timeout occurred during compilation or execution.\n")

    def go_next(self):
        self.canvas.destroy()
        self.go_next_validation()

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
        # Extract class name from "public class ClassName"
        class_name_start = java_class.index("public class") + len("public class")
        class_name_end = java_class.index("{", class_name_start)
        class_name = java_class[class_name_start:class_name_end].strip()
        return class_name
