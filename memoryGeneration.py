from main import RUTA
import json

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

file = open(RUTA, "r")
lineas = file.readlines()

# Resultado final
compiledOperands = []
toCompileOperands = []
variables = []
subroutines = []

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
    # Convierte cualquier operando en hexagesimal para compilarlo
    """
    operand_no_hashtag = operand[1:] if operand.startswith("#") else operand
    returnString = ""

    # If code is already in hex
    if operand_no_hashtag.startswith("$"):
        returnString = operand_no_hashtag[1:]

    # if code is in binary
    if operand_no_hashtag.startswith("%"):
        returnString =  str(hex(int(operand_no_hashtag[1:], 2))[2:]).upper()
    
    # if code is in octal
    if operand_no_hashtag.startswith("&"):
        returnString = str(hex(int(operand_no_hashtag[1:], 8))[2:]).upper()
    
    # if code is in decimal
    if operand_no_hashtag.isdigit():
        returnString = str(hex(int(operand_no_hashtag))[2:]).upper()

    return returnString

def compileInstructions():
    """
    # Compila instrucciones y agrega referencias a subrutinas
    """
    global lineas
    global variables
    operands = []
    global operandDict
    iteration = -1
    for line in lineas:
        iteration += 1
        operands = line.split()
        # Skipping empty lines and comments
        if len(line) == 0 or operands[0].startswith(("*")):
            continue
        # Skipping subroutine declaratoins
        if len(operands)==1 and operands[0] not in operandDict:
            continue
        # Beggining of the program
        if operands[1] == "ORG":
            global START_ADDRESS
            START_ADDRESS = convertOperand(operands[2])
        if operands[0] in operandDict:
            toCompileOperands.append(getOpcode(operands))
            addOperandHex(operands)




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
        comparisonLine = operandDict[line[0].lower()][3]-len(operandDict[line[0].lower()][2])/2
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
        operands = []
        if len(line) == 0 or operands[0].startswith(("*")):
            continue
        operands = line.split()
        if len(operands)==1 and operands[0] not in operandDict:
            subroutines.append(programSubroutine(operands[0], iteration))


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
        return convertOperand(skips)
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
        return convertOperand(int("".join(binRepresentationList), 2))



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


def compileFile():
    """
    # Función principal del módulo, se encarga de compilar el código
    - Recorre cada línea del código, y dependiendo del tipo de instrucción, la compila y la agrega a la lista de instrucciones compiladas
    """
    preCompile()
    compileInstructionSet(toCompileOperands)





