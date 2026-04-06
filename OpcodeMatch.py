import json


with open("opcode.json", "r") as f:
    opcodes = json.load(f)

with open("archivo.txt", "r") as f:
    lineas = f.readlines()

tieneEnd = False
contadorLineas = 0
esEtiqueta = False
errores = []

def verifyMatch():
    global contadorLineas, contadorErrores, tieneEnd, esEtiqueta
    esEtiqueta = False

    for l in lineas:
        contadorLineas += 1

        if l.startswith((" ", "\t")):
            partes = l.split()
            mnemonico = partes[0]
        else:
            partes = l.split()
            etiqueta = partes[0]

            if etiqueta.isupper() and etiqueta not in opcodes:
                esEtiqueta = True
            if len(partes) > 1:
                mnemonico = partes[1]

        if mnemonico.isupper() or mnemonico.islower():
            match = True if mnemonico.lower() in opcodes else False

        if not match and not esEtiqueta:
            errores.append(f"Línea {contadorLineas}: no se encontró el mnemónico {mnemonico}")

        

        
