import json

RUTA = ""

class programVar:
    """
    # Clase para variables 
    - usada para variables de tipo EQU y FCB, para facilitar su manejo
    ## Atributos
    - name: nombre de la variable
    - value: valor de la variable
    ## Métodos
    - value(): devuelve el valor de la variable
    """
    def __init__(self, name, value):
        self.name = name
        self.value = value 
    def value(self):
        return self.value
class programOperand:
    """
    # Clase para operandos
    - usada para operandos de instrucciones, para facilitar su manejo
    ## Atributos
    - name: nombre del operando
    - value: valor del operando
    ## Métodos
    - value(): devuelve el valor del operando
    """
    def __init__(self, name, value):
        self.name = name
        self.value = value 
    def value(self):
        return self.value
    def name(self):
        return self.name
class programSubroutine:
    """
    # Clase para subrutinas
    - usada para subrutinas, para facilitar su manejo
    ## Atributos
    - name: nombre de la subrutina
    - posicion: posicion relativa (con respecto al inicio del programa)
    ## Métodos
    - address(): devuelve la dirección de memoria de la subrutina
    """
    def __init__(self, name, posicion):
        self.name = name
        self.posicion = posicion 
    def address(self):
        return self.posicion
operandDict = json.load(open("opcode.json", "r"))

lineas = []

# Resultado final
compiledOperands = []
toCompileOperands = []
variables = []
subroutines = []
instructionList = []  # lista de tuplas (etiqueta, opcode, [operandos_hex], fuente)

START_ADDRESS = ""

def getcompiledOperands():
    """# Devuelve la lista de instrucciones ya compiladas
    - Cada operando es un String
    """
    global compiledOperands
    compileFile()
    return compiledOperands

def convertOperand(operand):
    """
    # Convierte cualquier operando en hexadecimal para compilarlo
    """
    operand_no_hashtag = operand[1:] if operand.startswith("#") else operand
    returnString = ""

    # Check if operand is a known variable (EQU)
    for var in variables:
        if var.name == operand_no_hashtag:
            return var.value

    # If code is already in hex
    if operand_no_hashtag.startswith("$"):
        returnString = operand_no_hashtag[1:]

    # if code is in binary
    if operand_no_hashtag.startswith("%"):
        returnString = str(hex(int(operand_no_hashtag[1:], 2))[2:]).upper()
    
    # if code is in octal
    if operand_no_hashtag.startswith("&"):
        returnString = str(hex(int(operand_no_hashtag[1:], 8))[2:]).upper()
    
    # if code is in decimal
    if operand_no_hashtag.isdigit():
        returnString = str(hex(int(operand_no_hashtag))[2:]).upper()

    return returnString

def compileInstructions():
    """
    # Compila instrucciones y registra posicion de subrutinas en bytes reales
    # Genera instructionList: lista de tuplas (etiqueta, opcode, [operandos], linea_fuente)
    """
    global lineas, variables, operandDict, subroutines, instructionList
    for line in lineas:
        lineaOriginal = line.rstrip("\r\n")
        operands = line.split()
        # Skipping empty lines and comments
        if len(operands) == 0 or operands[0].startswith("*"):
            continue
        # Remove inline comments
        if "*" in operands:
            operands = operands[:operands.index("*")]
        if len(operands) == 0:
            continue

        # Determine if line starts with a label or is indented
        lineStartsWithSpace = line.startswith((" ", "\t"))

        if lineStartsWithSpace:
            mnemonico = operands[0]
            resto = operands[1:]
            etiqueta = None
        else:
            etiqueta = operands[0]
            if len(operands) < 2:
                # Linea solo con etiqueta - registrar posicion actual en bytes
                for s in subroutines:
                    if s.name == etiqueta:
                        s.posicion = len(toCompileOperands)
                instructionList.append((etiqueta, None, [], ""))
                continue
            mnemonico = operands[1]
            resto = operands[2:]
            # Registrar posicion de la etiqueta antes de compilar su instruccion
            for s in subroutines:
                if s.name == etiqueta:
                    s.posicion = len(toCompileOperands)

        # Skip directives
        if mnemonico.upper() in ("ORG", "EQU", "FCB", "END"):
            if mnemonico.upper() == "ORG" and len(resto) > 0:
                global START_ADDRESS
                if START_ADDRESS == "":
                    START_ADDRESS = convertOperand(resto[0])
            continue

        # Skip if mnemonic is not in opcode dictionary
        if mnemonico.lower() not in operandDict:
            continue

        instruccion = [mnemonico] + resto
        opcode = getOpcode(instruccion)
        operandos_hex = []
        # Capture operand hex values without appending to toCompileOperands yet
        for i in instruccion[1:]:
            if i == 'X' or i == 'Y':
                continue
            if any(s.name == i for s in subroutines):
                operandos_hex.append(i)  # placeholder, resolved later
            else:
                operandos_hex.append(convertOperand(i))

        toCompileOperands.append(opcode)
        for op in operandos_hex:
            toCompileOperands.append(op)

        # Build source text for right column (mnemonic + original operands)
        fuenteTexto = mnemonico + (" " + " ".join(resto) if resto else "")
        instructionList.append((etiqueta, opcode, operandos_hex, fuenteTexto))




def getOpcode(line):
    """
    # Función para obtener el opcode de una instrucción
    # Se encarga de determinar el tipo de direccionamiento de la instrucción, y devolver el opcode correspondiente"""
    global operandDict
    opcode = ""

    # Modes with no shared mnemonics
        # Inherent addressing
    if operandDict[line[0].lower()][10] != 0:
        opcode = operandDict[line[0].lower()][10]
        # Relative addressing
    if operandDict[line[0].lower()][12] != 0:
        opcode = operandDict[line[0].lower()][12]
    # Inherent addressing
    for i in line:
        if i =="X":
            opcode = operandDict[line[0].lower()][4]
        if i =="Y":
            opcode = operandDict[line[0].lower()][6]
    # Immediate addressing
    if opcode =="":
        for i in line:
            if i.startswith("#"):
                opcode = operandDict[line[0].lower()][2]
    
    # Direct and extended addressing
    if opcode =="":
        imm_opcode = operandDict[line[0].lower()][2]
        if isinstance(imm_opcode, str):
            comparisonLine = operandDict[line[0].lower()][3] - len(imm_opcode) / 2
        else:
            comparisonLine = operandDict[line[0].lower()][3]
        if comparisonLine == len(line):
            opcode = operandDict[line[0].lower()][3]
        else:
            opcode = operandDict[line[0].lower()][8]
    return opcode

def addOperandHex(line):
    """
    # Función para obtener el operando de una instrucción en hexadecimal
    - Se encarga de determinar el tipo de direccionamiento de la instrucción, y devolver el operando correspondiente en hexadecimal
    """
    global toCompileOperands    
    operands = line[1:]
    for i in operands:
        if i== 'X' or i== 'Y':
            continue
        if any(subroutine.name == i for subroutine in subroutines):
            toCompileOperands.append(i)
        else:
            toCompileOperands.append(convertOperand(i))






def getSubroutines():
    """
    # Función para compilar las definiciones de subrutinas en el codigo
    - Añade la subrutina con el nombre y la posición (contada como índice) en la que aparece al declararse
    # """
    global lineas
    global subroutines
    iteration = -1
    for line in lineas:
        iteration += 1
        operands = line.split()
        if len(operands) == 0 or operands[0].startswith("*"):
            continue
        # Solo registrar nombre; posicion se actualiza en compileInstructions
        if not line.startswith((" ", "\t")):
            nombre = operands[0]
            if nombre.lower() not in operandDict and (len(operands) == 1 or operands[1].upper() not in ("EQU", "FCB", "ORG", "END")):
                subroutines.append(programSubroutine(nombre, 0))


def getVars():
    """
    # Función para compilar las variables declaradas en el código
    - Se encarga de convertir el valor de las variables a hexadecimal, y agregarlas a la lista de instrucciones compiladas
    """
    global lineas
    global variables
    for line in lineas:
        operands = line.split()
        if len(operands) == 0 or operands[0].startswith(("*")):
            continue
        if len(operands) < 2:
            continue
        if operands[1] == "EQU":
            variables.append(programVar(operands[0], convertOperand(operands[2])))


def countSkips( subroutine, position):
    """
    # Función para contar los bytes que se deben saltar para llegar a una subrutina
    - Se encarga de contar los bytes que se deben saltar para llegar a una subrutina, y actualizar la posición de la subrutina en la lista de instrucciones compiladas
    - Subroutine: nombre de subrutina a la cual saltar
    - Position: posición actual 
    """
    global subroutines
    subroutinePosition = 0
    for i in subroutines:
        if i.name == subroutine:
            subroutinePosition = i.posicion
    skips  = subroutinePosition - (position+1)
    return skips

def subRoutineHex(subroutine, position):
    """
    # Función para obtener el operando de una subrutina en hexadecimal
    - Se encarga de contar los bytes que se deben saltar para llegar a una subrutina, y devolver el operando correspondiente en hexadecimal
    - Subroutine: nombre de subrutina a la cual saltar
    - Position: posición actual 
    """
    skips = countSkips(subroutine, position)
    if skips>128 or skips<-127:
        return False
    if skips>0:
        return convertOperand(str(skips))
    else:
        return base2Compliment(skips)

def base2Compliment(number):
    """
    # Función para obtener el complemento a 2 de un número
    - Se encarga de obtener el complemento a 2 de un número, para poder representarlo en hexadecimal
    - Number: número al cual se le quiere obtener el complemento a 2
    """
    binRepresentation = bin(number)[2:]
    binRepresentationList = list(binRepresentation)
    for i in range(len(binRepresentationList)):
        if binRepresentationList[i] == "1":
            binRepresentationList[i] = "0"
        else:
            binRepresentationList[i] = "1"
    
    for i in range(len(binRepresentationList)-1, -1, -1):
        if binRepresentationList[i] == "0":
            binRepresentationList[i] = "1"
            break
        else:
            binRepresentationList[i] = "0"

    if number >= 0:
        return number
    else:
        return convertOperand(str(int("".join(binRepresentationList), 2)))



def compileInstructionSet(preCompilation):
    global compiledOperands
    position = -1
    for i in preCompilation:
        position += 1
        if any(subroutine.name == i for subroutine in subroutines):
            if subRoutineHex(i, position) == False:
                print(f"Error 007: Subrutina {i} fuera de rango")
                return False
            compiledOperands.append(subRoutineHex(i, position))
        else:
            compiledOperands.append(i)

        
def preCompile():
    """
    # Función para precompilar el código
    - Se encarga de compilar las variables declaradas en el código, y agregar las subrutinas a la lista de instrucciones compiladas
    """
    getVars()
    getSubroutines()
    compileInstructions()


def compileFile(ruta=None):
    """
    # Función principal del módulo, se encarga de compilar el código
    - Recorre cada línea del código, y dependiendo del tipo de instrucción, la compila y la agrega a la lista de instrucciones compiladas
    """
    global lineas, compiledOperands, toCompileOperands, variables, subroutines, instructionList, START_ADDRESS
    if ruta:
        with open(ruta, "r") as f:
            lineas = f.readlines()
    # Reset state
    compiledOperands = []
    toCompileOperands = []
    variables = []
    subroutines = []
    instructionList = []
    START_ADDRESS = ""
    preCompile()
    compileInstructionSet(toCompileOperands)

def generateOutput(outputPath=None):
    """
    # Genera el archivo de salida con formato:
    #                     ETIQUETA
    # XXXX XX XX          MNEM OPERANDOS
    """
    global instructionList, compiledOperands, START_ADDRESS, subroutines

    # Resolver direccion de inicio
    # Use first ORG address found
    try:
        currentAddress = int(START_ADDRESS, 16)
    except:
        currentAddress = 0x8000

    lines_out = []
    COL_WIDTH = 20

    for (etiqueta, opcode, operandos_hex, fuente) in instructionList:
        # Linea de solo etiqueta
        if opcode is None:
            lines_out.append(" " * COL_WIDTH + etiqueta)
            continue

        # Si hay etiqueta + instruccion, primero la etiqueta
        if etiqueta is not None:
            lines_out.append(" " * COL_WIDTH + etiqueta)

        # Resolver placeholders de subrutinas en operandos
        operandos_resueltos = []
        for op in operandos_hex:
            if any(s.name == op for s in subroutines):
                # calcular salto relativo
                skips = None
                for s in subroutines:
                    if s.name == op:
                        # posicion en toCompileOperands del destino
                        # contar bytes hasta esa posicion
                        skips = s.posicion - (len(operandos_resueltos) + 1)
                if skips is not None:
                    if skips >= 0:
                        operandos_resueltos.append(format(skips, '02X'))
                    else:
                        operandos_resueltos.append(format(skips & 0xFF, '02X'))
            else:
                operandos_resueltos.append(op.upper() if op else "??")

        # Construir bytes de la instruccion
        # opcode puede ser "8B" (1 byte) o "18CE" (2 bytes prefijados)
        opcode_bytes = [opcode[i:i+2] for i in range(0, len(str(opcode)), 2)] if isinstance(opcode, str) else [format(opcode, '02X')]
        # operandos: cada string de 2 chars es 1 byte, 4 chars es 2 bytes
        operando_bytes = []
        for op in operandos_resueltos:
            for i in range(0, len(op), 2):
                operando_bytes.append(op[i:i+2])

        all_bytes = opcode_bytes + operando_bytes
        n_bytes = len(all_bytes)

        addr_str = format(currentAddress & 0xFFFF, '04X')
        bytes_str = " ".join(all_bytes)
        left_col = f"{addr_str} {bytes_str}"
        left_col = left_col.ljust(COL_WIDTH)

        lines_out.append(left_col + fuente)
        currentAddress += n_bytes

    resultado = "\n".join(lines_out)

    if outputPath:
        with open(outputPath, "w") as f:
            f.write(resultado)

    return resultado