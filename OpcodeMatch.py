import json

with open("opcode.json", "r") as f:
    opcodes = json.load(f)

tieneEnd = False
contadorLineas = 0
esEtiqueta = False
errores = []
orgs = []


SALTOS = {"bra", "beq", "bne", "blt", "ble", "bgt", "bge", "bhi", "bhs",
          "blo", "bls", "bmi", "bpl", "bvc", "bvs", "bcc", "bcs", "brn",
          "jmp", "jsr", "bsr", "brset", "brclr"}

REFS_ETIQUETA = SALTOS

    
def recolectarDeclaraciones(lineas):
    declaradas = set()
    etiquetas = set()
    
    for l in lineas:
        lineaOriginal = l
        l = l.strip()

        if not l or l.startswith(("*", ";")):
            continue
        if "*" in l:
            l = l[:l.index("*")].strip()

        partes = l.split()

        if not lineaOriginal.startswith((" ", "\t")):
            nombre = partes[0].upper()

            if len(partes) >= 3 and partes[1].upper() in ("EQU", "FCB"):
                declaradas.add(nombre)
            elif len(partes) == 1 or partes[1].upper() not in ("EQU", "FCB", "ORG", "END"):
                etiquetas.add(nombre)

    return declaradas, etiquetas


def verifyMatch(file):
    global contadorLineas, tieneEnd, esEtiqueta, errores, orgs

    with open(file, "r") as f:
        lineas = f.readlines()

    declaradas, etiquetas = recolectarDeclaraciones(lineas)
        
    for l in lineas:
        esEtiqueta = False
        contadorLineas += 1
        mnemonico = None
        operandos = []

        lineaOriginal = l
        l = l.strip()

        if not l or l.startswith(("*", ";")):
            continue
        if "*" in l:
            l = l[:l.index("*")].strip()

        partes = l.split()

        if not lineaOriginal.startswith((" ", "\t")):
            nombre = partes[0].upper()
            if nombre.lower() in opcodes and nombre not in etiquetas:
                errores.append(f"Línea {contadorLineas}: Error 009 mnemónico '{partes[0]}' debe ir precedido de al menos un espacio o tabulación")
                continue

            etiqueta = partes[0]
            if etiqueta.upper() == etiqueta and etiqueta.lower() not in opcodes:
                esEtiqueta = True
            if len(partes) > 1:
                mnemonico = partes[1]
                operandos = partes[2:]
        else:
            mnemonico = partes[0]
            operandos = partes[1:]

        if mnemonico and mnemonico.upper() == "ORG":
            if operandos:
                orgs.append([operandos[0].replace("$", ""),contadorLineas])
            continue
        if mnemonico and mnemonico.upper() in ("EQU", "FCB"):
            continue

        if mnemonico and mnemonico.upper() == "END":
            tieneEnd = True
            break

        if mnemonico and (mnemonico.isupper() or mnemonico.islower()):
            match = mnemonico.lower() in opcodes
            if not match and not esEtiqueta:
                errores.append(f"Línea {contadorLineas}: Error 004 no se encontró el mnemónico '{mnemonico}'")

        for operando in operandos:
            if operando.startswith(("#", "$")):
                continue
            operando_limpio = operando.strip(",#$").upper()

            if not operando_limpio.isalpha():
                continue

            es_ref_etiqueta = mnemonico and mnemonico.lower() in REFS_ETIQUETA

            if es_ref_etiqueta:
                if operando_limpio in etiquetas:
                    continue
                if operando_limpio not in etiquetas:
                    errores.append(f"Línea {contadorLineas}: Error 003 etiqueta '{operando_limpio}' no declarada")
            else:
                if operando_limpio in declaradas:
                    continue
                if operando_limpio.lower() in opcodes:
                    continue 
                if operando_limpio not in declaradas:
                    errores.append(f"Línea {contadorLineas}: Error 001 variable o constante '{operando_limpio}' no declarada")

    if not tieneEnd:
        errores.append("Error 010: falta la directiva END al final del programa")
    
    if len(errores) == 0:
        return "Compilación exitosa", [], orgs
    else:
        return "Error en compilación", errores, orgs