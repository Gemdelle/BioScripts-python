def agregar_saltos_de_linea(texto, limite=80):
    palabras = texto.split()
    caracteres_actuales = 0
    texto_con_saltos = ''

    for palabra in palabras:
        caracteres_actuales += len(palabra) + 1
        if caracteres_actuales > limite:
            texto_con_saltos += '\n'
            caracteres_actuales = len(palabra) + 1
        texto_con_saltos += palabra + ' '

    return texto_con_saltos.strip()