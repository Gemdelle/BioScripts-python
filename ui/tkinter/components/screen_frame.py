import tkinter as tk

from core.screens import Screens
from ui.screens import splash, win_emblem
from ui.screens.headers import programme, landing, landing_2, programme_1, book, programme_2, programme_3, \
    notes
from ui.screens.arrays import arrays_0, arrays_1, arrays_2, arrays_3, arrays_4, arrays_5, arrays_6, arrays_7, arrays_8, \
    arrays_9, arrays_10, arrays_11, arrays_12, arrays_13, arrays_14, arrays_15, arrays_16, arrays_17, arrays_18, \
    arrays_19, arrays_20, arrays_21, arrays_22, arrays_23, arrays_24, arrays_25, arrays_26
from ui.screens.asignacion_screens import asignacion_0, asignacion_1, asignacion_2, asignacion_3, asignacion_4, \
    asignacion_5, asignacion_test
from ui.screens.comentarios_screens import comentarios_0, comentarios_1, comentarios_2, comentarios_3, comentarios_4, \
    comentarios_test
from ui.screens.headers.book import library, library_1, library_2, library_3, library_4, library_5, library_6, \
    library_7, library_8, library_9, library_10, library_11, library_12, library_13, library_14, library_15, library_16, \
    library_17, library_18, library_19, library_20
from ui.screens.input_screens import input_0, input_1, input_2, input_test
from ui.screens.operaciones_aritmeticas import operaciones_aritmeticas_0, operaciones_aritmeticas_1, \
    operaciones_aritmeticas_2, operaciones_aritmeticas_3, operaciones_aritmeticas_4, operaciones_aritmeticas_5, \
    operaciones_aritmeticas_6, operaciones_aritmeticas_7, operaciones_aritmeticas_8
from ui.screens.operaciones_comparacion import operaciones_comparacion_0, operaciones_comparacion_1, \
    operaciones_comparacion_2, operaciones_comparacion_3, operaciones_comparacion_4, operaciones_comparacion_5
from ui.screens.print_screens import print_0, print_1, print_2, print_3, print_4, print_test, print_5, print_6
from ui.screens.transformacion_screens import transformacion_0, transformacion_1, transformacion_test, transformacion_2, \
    transformacion_3

screen_draw_functions = {
    Screens.SPLASH: splash.draw,
    Screens.LANDING: landing.draw,
    Screens.LANDING_2: landing_2.draw,
    Screens.LIBRARY: library.draw,
    Screens.LIBRARY_1: library_1.draw,
    Screens.LIBRARY_2: library_2.draw,
    Screens.LIBRARY_3: library_3.draw,
    Screens.LIBRARY_4: library_4.draw,
    Screens.LIBRARY_5: library_5.draw,
    Screens.LIBRARY_6: library_6.draw,
    Screens.LIBRARY_7: library_7.draw,
    Screens.LIBRARY_8: library_8.draw,
    Screens.LIBRARY_9: library_9.draw,
    Screens.LIBRARY_10: library_10.draw,
    Screens.LIBRARY_11: library_11.draw,
    Screens.LIBRARY_12: library_12.draw,
    Screens.LIBRARY_13: library_13.draw,
    Screens.LIBRARY_14: library_14.draw,
    Screens.LIBRARY_15: library_15.draw,
    Screens.LIBRARY_16: library_16.draw,
    Screens.LIBRARY_17: library_17.draw,
    Screens.LIBRARY_18: library_18.draw,
    Screens.LIBRARY_19: library_19.draw,
    Screens.LIBRARY_20: library_20.draw,
    Screens.NOTES: notes.draw,
    Screens.PROGRAMME: programme.draw,
    Screens.PROGRAMME_1: programme_1.draw,
    Screens.PROGRAMME_2: programme_2.draw,
    Screens.PROGRAMME_3: programme_3.draw,
    Screens.WIN_EMBLEM: win_emblem.draw,
    Screens.COMENTARIOS_0: comentarios_0.draw,
    Screens.COMENTARIOS_1: comentarios_1.draw,
    Screens.COMENTARIOS_2: comentarios_2.draw,
    Screens.COMENTARIOS_3: comentarios_3.draw,
    Screens.COMENTARIOS_4: comentarios_4.draw,
    Screens.COMENTARIOS_TEST: comentarios_test.draw,
    Screens.PRINT_0: print_0.draw,
    Screens.PRINT_1: print_1.draw,
    Screens.PRINT_2: print_2.draw,
    Screens.PRINT_3: print_3.draw,
    Screens.PRINT_4: print_4.draw,
    Screens.PRINT_5: print_5.draw,
    Screens.PRINT_6: print_6.draw,
    Screens.PRINT_TEST: print_test.draw,
    Screens.ASIGNACION_0: asignacion_0.draw,
    Screens.ASIGNACION_1: asignacion_1.draw,
    Screens.ASIGNACION_2: asignacion_2.draw,
    Screens.ASIGNACION_3: asignacion_3.draw,
    Screens.ASIGNACION_4: asignacion_4.draw,
    Screens.ASIGNACION_5: asignacion_5.draw,
    Screens.ASIGNACION_TEST: asignacion_test.draw,
    Screens.TRANSFORMACION_0: transformacion_0.draw,
    Screens.TRANSFORMACION_1: transformacion_1.draw,
    Screens.TRANSFORMACION_2: transformacion_2.draw,
    Screens.TRANSFORMACION_3: transformacion_3.draw,
    Screens.TRANSFORMACION_TEST: transformacion_test.draw,
    Screens.INPUT_0: input_0.draw,
    Screens.INPUT_1: input_1.draw,
    Screens.INPUT_2: input_2.draw,
    Screens.INPUT_TEST: input_test.draw,
    Screens.OPERACIONES_ARITMETICAS_0: operaciones_aritmeticas_0.draw,
    Screens.OPERACIONES_ARITMETICAS_1: operaciones_aritmeticas_1.draw,
    Screens.OPERACIONES_ARITMETICAS_2: operaciones_aritmeticas_2.draw,
    Screens.OPERACIONES_ARITMETICAS_3: operaciones_aritmeticas_3.draw,
    Screens.OPERACIONES_ARITMETICAS_4: operaciones_aritmeticas_4.draw,
    Screens.OPERACIONES_ARITMETICAS_5: operaciones_aritmeticas_5.draw,
    Screens.OPERACIONES_ARITMETICAS_6: operaciones_aritmeticas_6.draw,
    Screens.OPERACIONES_ARITMETICAS_7: operaciones_aritmeticas_7.draw,
    Screens.OPERACIONES_ARITMETICAS_8: operaciones_aritmeticas_8.draw,
    # Screens.OPERACIONES_ARITMETICAS_TEST: operaciones_aritmeticas_test.draw,
    Screens.OPERACIONES_COMPARACION_0: operaciones_comparacion_0.draw,
    Screens.OPERACIONES_COMPARACION_1: operaciones_comparacion_1.draw,
    Screens.OPERACIONES_COMPARACION_2: operaciones_comparacion_2.draw,
    Screens.OPERACIONES_COMPARACION_3: operaciones_comparacion_3.draw,
    Screens.OPERACIONES_COMPARACION_4: operaciones_comparacion_4.draw,
    Screens.OPERACIONES_COMPARACION_5: operaciones_comparacion_5.draw,
    # Screens.OPERACIONES_COMPARACION_TEST: operaciones_comparacion_test.draw,
    # Screens.BUCLE_IF_0: bucle_if_0.draw,
    # Screens.BUCLE_IF_1: bucle_if_1.draw,
    # Screens.BUCLE_IF_2: bucle_if_2.draw,
    # Screens.BUCLE_IF_3: bucle_if_3.draw,
    # Screens.BUCLE_IF_4: bucle_if_4.draw,
    # Screens.BUCLE_IF_5: bucle_if_5.draw,
    # Screens.BUCLE_IF_6: bucle_if_6.draw,
    # Screens.BUCLE_IF_7: bucle_if_7.draw,
    # Screens.BUCLE_IF_8: bucle_if_8.draw,
    # Screens.BUCLE_IF_9: bucle_if_9.draw,
    # Screens.BUCLE_IF_10: bucle_if_10.draw,
    # Screens.BUCLE_IF_11: bucle_if_11.draw,
    # Screens.BUCLE_IF_12: bucle_if_12.draw,
    # Screens.BUCLE_IF_13: bucle_if_13.draw,
    # Screens.BUCLE_IF_14: bucle_if_14.draw,
    # Screens.BUCLE_IF_15: bucle_if_15.draw,
    # Screens.BUCLE_IF_16: bucle_if_16.draw,
    # Screens.BUCLE_IF_17: bucle_if_17.draw,
    # Screens.BUCLE_IF_18: bucle_if_18.draw,
    # Screens.BUCLE_IF_TEST: bucle_if_test.draw,
    Screens.ARRAYS_0: arrays_0.draw,
    Screens.ARRAYS_1: arrays_1.draw,
    Screens.ARRAYS_2: arrays_2.draw,
    Screens.ARRAYS_3: arrays_3.draw,
    Screens.ARRAYS_4: arrays_4.draw,
    Screens.ARRAYS_5: arrays_5.draw,
    Screens.ARRAYS_6: arrays_6.draw,
    Screens.ARRAYS_7: arrays_7.draw,
    Screens.ARRAYS_8: arrays_8.draw,
    Screens.ARRAYS_9: arrays_9.draw,
    Screens.ARRAYS_10: arrays_10.draw,
    Screens.ARRAYS_11: arrays_11.draw,
    Screens.ARRAYS_12: arrays_12.draw,
    Screens.ARRAYS_13: arrays_13.draw,
    Screens.ARRAYS_14: arrays_14.draw,
    Screens.ARRAYS_15: arrays_15.draw,
    Screens.ARRAYS_16: arrays_16.draw,
    Screens.ARRAYS_17: arrays_17.draw,
    Screens.ARRAYS_18: arrays_18.draw,
    Screens.ARRAYS_19: arrays_19.draw,
    Screens.ARRAYS_20: arrays_20.draw,
    Screens.ARRAYS_21: arrays_21.draw,
    Screens.ARRAYS_22: arrays_22.draw,
    Screens.ARRAYS_23: arrays_23.draw,
    Screens.ARRAYS_24: arrays_24.draw,
    Screens.ARRAYS_25: arrays_25.draw,
    Screens.ARRAYS_26: arrays_26.draw,
    # Screens.ARRAYS_TEST: arrays_test.draw,
    # Screens.FOR_0: for_0.draw,
    # Screens.FOR_1: for_1.draw,
    # Screens.FOR_2: for_2.draw,
    # Screens.FOR_3: for_3.draw,
    # Screens.FOR_4: for_4.draw,
    # Screens.FOR_TEST: for_test.draw,
    # Screens.WHILE_0: while_0.draw,
    # Screens.WHILE_1: while_1.draw,
    # Screens.WHILE_2: while_2.draw,
    # Screens.WHILE_3: while_3.draw,
    # Screens.WHILE_4: while_4.draw,
    # Screens.WHILE_5: while_5.draw,
    # Screens.WHILE_6: while_6.draw,
    # Screens.WHILE_TEST: while_test.draw,
    # Screens.FUNCIONES_0: funciones_0.draw,
    # Screens.FUNCIONES_1: funciones_1.draw,
    # Screens.FUNCIONES_2: funciones_2.draw,
    # Screens.FUNCIONES_3: funciones_3.draw,
    # Screens.FUNCIONES_4: funciones_4.draw,
    # Screens.FUNCIONES_5: funciones_5.draw,
    # Screens.FUNCIONES_6: funciones_6.draw,
    # Screens.FUNCIONES_7: funciones_7.draw,
    # Screens.FUNCIONES_8: funciones_8.draw,
    # Screens.FUNCIONES_9: funciones_9.draw,
    # Screens.FUNCIONES_10: funciones_10.draw,
    # Screens.FUNCIONES_11: funciones_11.draw,
    # Screens.FUNCIONES_12: funciones_12.draw,
    # Screens.FUNCIONES_13: funciones_13.draw,
    # Screens.FUNCIONES_14: funciones_14.draw,
    # Screens.FUNCIONES_TEST: funciones_test.draw,
}


class ScreenFrame(tk.Frame):
    def __init__(self, master, screen, change_screen):
        super().__init__(master, width=1280, height=720, bg="#6d6f77")
        self.pack_propagate(False)
        self.change_screen = change_screen
        self.draw_function = screen_draw_functions.get(screen)

    def draw(self):
        if self.draw_function:
            self.draw_function(self, self.change_screen)