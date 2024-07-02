from ui.tkinter.screens.father_game import FatherGame
from ui.tkinter.screens.father_validation_1 import FatherValidation1
from ui.tkinter.screens.father_validation_2 import FatherValidation2
from ui.tkinter.screens.father_validation_3 import FatherValidation3


class FatherScreen:
    def __init__(self, root, close_app):
        self.root = root
        self.root.title("Father Screen")
        self.close_app = close_app
        self.validation_canvas = FatherValidation1(
            self.root,
            self.go_to_validation_2
        )

    def go_to_validation_2(self):
        self.validation_canvas = FatherValidation2(
            self.root,
            self.go_to_validation_3
        )
    def go_to_validation_3(self):
        self.validation_canvas = FatherValidation3(
            self.root,
            self.go_to_father_game
        )
    def go_to_father_game(self):
        self.validation_canvas = FatherGame(
            self.root,
            self.close_app
        )
