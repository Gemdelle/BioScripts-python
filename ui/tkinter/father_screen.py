import subprocess
import tkinter as tk
from tkinter import scrolledtext

from PIL import Image, ImageTk

from utils.resource_path_util import resource_path


class FatherScreen:
    def __init__(self, root):
        self.root = root
        self.root.title("Father Screen")
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
        self.input_text = scrolledtext.ScrolledText(self.root, width=55, height=35, bg='#fefbe6', borderwidth=0, highlightthickness=0, wrap=tk.NONE)
        self.input_text.config(xscrollcommand=None, yscrollcommand=None)  # Disable both horizontal and vertical scrollbars
        self.canvas.create_window(100, 150, anchor='nw', window=self.input_text)

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

        # Output label
        self.output_label = tk.Label(self.root, text="Output:")
        self.canvas.create_window(640, 760, anchor='nw', window=self.output_label)

        # Output text area
        self.output_text = scrolledtext.ScrolledText(self.root, width=60, height=10)
        self.canvas.create_window(640, 780, anchor='nw', window=self.output_text)

    def scroll_text(self, event):
        if event.keysym == "Up":
            self.input_text.yview_scroll(-1, "units")
        elif event.keysym == "Down":
            self.input_text.yview_scroll(1, "units")

    def run_java_code(self, event):
        print("LLEGO!")
        return
        java_code = self.input_text.get("1.0", tk.END)

        # Split the Java code into individual class definitions based on "//----------"
        java_classes = self.split_java_classes(java_code)

        compile_processes = []

        for java_class in java_classes:
            if java_class.strip().startswith("public class"):
                # Extract class name
                class_name = self.extract_class_name(java_class)

                # Write the Java file
                with open(f"{class_name}.java", "w") as file:
                    file.write(java_class)

                # Compile the Java file
                compile_process = subprocess.Popen(["javac", f"{class_name}.java"], stdout=subprocess.PIPE,
                                                   stderr=subprocess.PIPE)
                compile_processes.append((class_name, compile_process))

        try:
            # Wait for all compilation processes to finish
            for class_name, compile_process in compile_processes:
                compile_process.wait(timeout=15)

                # Check compilation result
                if compile_process.returncode != 0:
                    self.output_text.insert(tk.END,
                                            f"Compilation Error for {class_name}.java:\n{compile_process.stderr.read().decode()}\n")
                    return

            # If compilation successful, execute the main method of Main class if exists
            if not any(class_name == "Main" for class_name, _ in compile_processes):
                self.output_text.insert(tk.END, "No Main class found.\n")
                return

            main_process = subprocess.Popen(["java", "Main"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            main_process.wait(timeout=15)

            # Display output of main execution
            if main_process.returncode == 0:
                self.output_text.delete("1.0", tk.END)
                self.output_text.insert(tk.END, "Execution successful.\n")
                self.output_text.insert(tk.END, main_process.stdout.read().decode())
            else:
                self.output_text.delete("1.0", tk.END)
                self.output_text.insert(tk.END, "Error occurred during execution.\n")
                self.output_text.insert(tk.END, main_process.stderr.read().decode())

        except subprocess.TimeoutExpired:
            self.output_text.delete("1.0", tk.END)
            self.output_text.insert(tk.END, "Timeout occurred during compilation or execution.\n")

    def split_java_classes(self, java_code):
        java_classes = []
        current_class = ""

        for line in java_code.splitlines():
            if line.strip() == "//":  # Class limiter
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