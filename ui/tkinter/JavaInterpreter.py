import tkinter as tk
from tkinter import scrolledtext
import subprocess

class JavaInterpreterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Java Code Interpreter")

        self.input_label = tk.Label(root, text="Enter Java code:")
        self.input_label.pack()

        self.input_text = scrolledtext.ScrolledText(root, width=60, height=20)
        self.input_text.pack()

        self.run_button = tk.Button(root, text="Run Code", command=self.run_java_code)
        self.run_button.pack()

        self.output_label = tk.Label(root, text="Output:")
        self.output_label.pack()

        self.output_text = scrolledtext.ScrolledText(root, width=60, height=10)
        self.output_text.pack()

    def run_java_code(self):
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