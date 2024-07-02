import subprocess
import tkinter as tk
from tkinter import scrolledtext

from PIL import Image, ImageTk

from ui.tkinter.components.gif_image import AnimatedGIF
from utils.constants import Constants
from utils.resource_path_util import resource_path
from utils.set_time_out_manager import SetTimeoutManager

class FatherValidation3:
    def __init__(self, root, go_next_validation):
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
        self.input_text.insert(tk.END, Constants.INITIAL_FATHER_VALIDATION_3_TEXT)
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

        # Initial GIF
        self.father_gif_root = resource_path("assets\\gifs\\father\\father_default_grey.gif")
        self.animated_gif = AnimatedGIF(self.canvas, self.father_gif_root, 740, 180)
        self.animated_gif.start_animation()

        task_bar_image = Image.open(resource_path("assets\\images\\task-bar.png"))
        task_bar_image = task_bar_image.resize((408, 1080))
        task_bar_image_tk = ImageTk.PhotoImage(task_bar_image)
        setattr(self.canvas, f"task_bar_image_tk", task_bar_image_tk)
        self.canvas.create_image(screen_width - 408, screen_height - 1080, anchor='nw', image=task_bar_image_tk, tags="task_bar")

        instructions_image = Image.open(resource_path("assets\\images\\instructions.png"))
        instructions_image = instructions_image.resize((1150, 300))
        instructions_image_tk = ImageTk.PhotoImage(instructions_image)
        setattr(self.canvas, f"instructions_image_tk", instructions_image_tk)
        self.canvas.create_image(screen_width - 1150, 0, anchor='nw', image=instructions_image_tk, tags="instructions")

        self.canvas.create_text(screen_width - 950, 25, text="Your text here", font=("Helvetica", 16), fill="black")

    def scroll_text(self, event):
        if event.keysym == "Up":
            self.input_text.yview_scroll(-1, "units")
        elif event.keysym == "Down":
            self.input_text.yview_scroll(1, "units")

    def update_gif(self, new_gif_path, start_frame, end_frame):
        self.animated_gif.destroy()
        self.animated_gif = AnimatedGIF(self.canvas, new_gif_path, 740, 180, start_frame=start_frame, end_frame=end_frame)
        self.animated_gif.start_animation()

    def get_input_text(self):
        return self.input_text.get("1.0", tk.END)

    def run_java_code(self, event):
        setTimeoutManager = SetTimeoutManager()
        java_code = self.get_input_text()

        # Split the Java code into individual class definitions based on "//---"
        java_classes = self.split_java_classes(java_code)

        compile_processes = []

        for java_class in java_classes:
            if java_class.strip().startswith("public class"):
                # Extract class name
                class_name = self.extract_class_name(java_class)

                # Write the Java file
                with open(f"./validations/father_validation_3/{class_name}.java", "w") as file:
                    file.write(java_class)

                # Compile the Java file
                compile_process = subprocess.Popen(["javac", f"{class_name}.java"], stdout=subprocess.PIPE,
                                                   stderr=subprocess.PIPE, cwd="./validations/father_validation_3")
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
                ["java", "MainFatherValidation1"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                cwd="./validations/father_validation_1"
            )
            main_process.wait(timeout=15)

            # Display output of main execution
            if main_process.returncode == 0:
                self.output_text.delete("1.0", tk.END)
                self.output_text.insert(tk.END, "Execution successful.\n")
                self.output_text.insert(tk.END, main_process.stdout.read().decode())
                self.update_gif(resource_path("assets\\gifs\\father\\father_default_new_correct.gif"), start_frame=1, end_frame=169)
                setTimeoutManager.setTimeout(lambda: self.update_gif(resource_path("assets\\gifs\\father\\father_default_correct.gif"), start_frame=1, end_frame=373), 2)
                setTimeoutManager.setTimeout(lambda: self.go_next(), 4)
            else:
                self.output_text.delete("1.0", tk.END)
                self.output_text.insert(tk.END, "Error occurred during execution.\n")
                self.output_text.insert(tk.END, main_process.stderr.read().decode())
                self.update_gif(resource_path("assets\\gifs\\father\\father_default_new_incorrect.gif"), start_frame=1, end_frame=149)
                setTimeoutManager.setTimeout(lambda: self.update_gif(resource_path("assets\\gifs\\father\\father_default_incorrect.gif"), start_frame=1, end_frame=373), 2)

        except subprocess.TimeoutExpired:
            self.output_text.delete("1.0", tk.END)
            self.output_text.insert(tk.END, "Timeout occurred during compilation or execution.\n")
            self.update_gif(resource_path("assets\\gifs\\father\\father_default_new_incorrect.gif"), start_frame=1, end_frame=149)
            setTimeoutManager.setTimeout(lambda: self.update_gif(resource_path("assets\\gifs\\father\\father_default_incorrect.gif"), start_frame=1, end_frame=373), 2)

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