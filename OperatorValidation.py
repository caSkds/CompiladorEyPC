import json

SALTOS = {"bra", "beq", "bne", "blt", "ble", "bgt", "bge", "bhi", "bhs",
          "blo", "bls", "bmi", "bpl", "bvc", "bvs", "bcc", "bcs", "brn",
          "jmp", "jsr", "bsr", "brset", "brclr"}

def instructionByteCount(operandName):
    return len(operandName) // 2 

def printFile(RUTA):
    file = open(RUTA, "r")
    lineas = file.readlines()
    endReached = False
    operandDict = json.load(open("opcode.json", "r"))

    global breakBool
    currOperandList = []
    breakBool = False
    nOperands = 0
    alwaysSmaller = True
    alwaysBigger = True
    lineCounter = 0

    errores = []

    for line in lineas:
        alwaysSmaller = True 
        alwaysBigger = True
        nOperands = 0
        currOperandList = []
        lineCounter += 1

        # Skipping empty lines
        if len(line.strip()) == 0:
            continue

        operands = line.split()

        if len(operands) == 0:
            continue

        # Skipping comments
        if operands[0].startswith("*"):
            continue

        # Removing ending comments
        for i in range(len(operands)):
            if operands[i].startswith("*"):
                operands = operands[:i]
                break

        if len(operands) == 0:
            continue
        
        if operands[0].lower() in SALTOS:
            continue
        # Special cases
        if operands[0] == "ORG":
            if len(operands) < 2:
                errores.append(f"Línea {lineCounter}: Error 005 Instrucción carece de operandos")
            elif len(operands) > 2:
                errores.append(f"Línea {lineCounter}: Error 006 Instrucción no lleva operandos")
            continue

        if operands[0] == "END":
            endReached = True
            if len(operands) > 1:
                errores.append(f"Línea {lineCounter}: Error 006 Instrucción no lleva operandos")
            continue

        if operands[0] == "EQU":
            if len(operands) < 3:
                errores.append(f"Línea {lineCounter}: Error 005 Instrucción carece de operandos")
            elif len(operands) > 3:
                errores.append(f"Línea {lineCounter}: Error 006 Instrucción no lleva operandos")
            continue

        # Checking for addressing modes
        operands[0] = operands[0].lower()
        if operands[0] not in operandDict:
            continue
        #Inherent addressing
        currOperandList = operandDict[operands[0]]
        if len(operands) == 1:
            if currOperandList[11] != 0:
                continue
            else:
                errores.append(f"Línea {lineCounter}: Error 005 Instrucción carece de operandos")
                continue
        #Immediate addressing
        if len(operands) > 1 and operands[1].startswith("#"):
            if currOperandList[1] == 0:
                errores.append(f"Línea {lineCounter}: Error 006 Instrucción no lleva operandos")
            continue
        #Indexed addressing with respect to X and Y
        for i in operands:
            if i == "X":
                if currOperandList[5] == 0:
                    errores.append(f"Línea {lineCounter}: Error 006 Instrucción no lleva operandos")
                if len(operands) > 1:
                    nOperands = currOperandList[5]
                    if len(operands) > nOperands + 2:
                        errores.append(f"Línea {lineCounter}: Error 006 Instrucción no lleva operandos")
                    if len(operands) < nOperands + 2:
                        errores.append(f"Línea {lineCounter}: Error 005 Instrucción carece de operandos")
                breakBool = True

            if i == "Y":
                if currOperandList[7] == 0:
                    errores.append(f"Línea {lineCounter}: Error 006 Instrucción no lleva operandos")
                if len(operands) > 1:
                    nOperands = currOperandList[7]
                    if len(operands) > nOperands + 2:
                        errores.append(f"Línea {lineCounter}: Error 006 Instrucción no lleva operandos")
                    if len(operands) < nOperands + 2:
                        errores.append(f"Línea {lineCounter}: Error 005 Instrucción carece de operandos")
                breakBool = True

        if breakBool:
            breakBool = False
            continue

        if len(operands) == 2:
            continue
        match = False

        for i in range(1, len(currOperandList), 2):
            if operands[1].startswith("#"):
                nOperands = currOperandList[i] - instructionByteCount(operands[1])
            else:
                nOperands = currOperandList[i]

            if len(operands) == nOperands + 1:
                match = True
                break

            if len(operands) < nOperands + 1:
                alwaysBigger = False
            if len(operands) > nOperands + 1:
                alwaysSmaller = False

        if not match:
            if alwaysSmaller and not alwaysBigger:
                errores.append(f"Línea {lineCounter}: Error 005 Instrucción carece de operandos")
            elif alwaysBigger and not alwaysSmaller:
                errores.append(f"Línea {lineCounter}: Error 006 Instrucción no lleva operandos")
            else:
                errores.append(f"Línea {lineCounter}: Error 006 Instrucción no válida")

    return errores