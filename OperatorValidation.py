from main import RUTA
import json

file = open(RUTA, "r")
lineas = file.readlines()
endReached = False
operandDict = json.load(open("opcode.json", "r"))
def instructionByteCount(operandName):
    return len(operandName)/2
def printFile():
    global breakBool
    global operandDict
    currOperandList= []
    breakBool = False
    nOperands = 0
    alwaysSmaller = True
    alwaysBigger = True    

    for line in lineas:
        alwaysSmaller = False
        alwaysBigger = False
        nOperands = 0
        currOperandList = []
        # Skipping empty lines
        if len(line) == 0:
            continue
        operands = line.split()
        if len(operands) == 0:
            continue
        #Skipping comments
        if operands[0].startswith(("*")):
            continue
        # Removing ending commments
        for i in range(len(operands)):
            if operands[i].startswith(("*")):
                operands = operands[:i]
                break
        #Special cases
        if (operands[0] == "ORG"):
            if len(operands) <2:
                print("Error 005: Instrucci´on carece de operandos")
            if len(operands) > 2:
                # Exceso de operandos
                print("Error 006: Instrucción no lleva operandos")
        if (operands[0] == "END"):
            endReached = True
            if len(operands) > 1:
                print("Error 006: Instrucción no lleva operandos") 
        if operands[0]=="EQU":
            if len(operands) < 3:
                print("Error 005: Instrucción carece de operandos")
            if len(operands) > 3:
                print("Error 006: Instrucción no lleva operandos")

        # Checking for addressing modes
        operands[0] = operands[0].lower()
        if (operands[0].lower() not in operandDict):
            continue

        #Inherent addressing
        currOperandList = operandDict[operands[0].lower()]
        if currOperandList[11] != 0:
            pass
        else:
            if len(operands)==1 :
                continue
            else:
                print("Error 005: Instrucción carece de operandos")
            continue
        #Immediate addressing
        if (operands[1].startswith("#")):
            if (currOperandList[1] == 0):
                print("Error 006: Instrucción no lleva operandos ")
            nOperands = currOperandList[1]-instructionByteCount(operands[1])
            if len(operands) > nOperands+1:
                print("Error 006: Instrucción no lleva operandos")
            if len(operands) < nOperands+1:
                print("Error 005: Instrucción carece de operandos")
            continue

        #Indexed addressing with respect to X and Y
        for i in operands:
            if i =="X":
                if (currOperandList[5] == 0):
                    print("Error 006: Instrucción no lleva operandos ")
                nOperands = currOperandList[5]-instructionByteCount(i)
                if len(operands) > nOperands+2:
                    print("Error 006: Instrucción no lleva operandos")
                if len(operands) < nOperands+2:
                    print("Error 005: Instrucción carece de operandos")
                breakBool = True
            if i =="Y":
                if (currOperandList[7] == 0):
                    print("Error 006: Instrucción no lleva operandos ")
                nOperands = currOperandList[7]-instructionByteCount(i)
                if len(operands) > nOperands+2:
                    print("Error 006: Instrucción no lleva operandos")
                if len(operands) < nOperands+2:
                    print("Error 005: Instrucción carece de operandos")
                breakBool = True
            
        if breakBool:
            breakBool = False
            continue

        #Checking for external, direct or inherent addressing modes
        
        for i in range(1, len(currOperandList),2):
            nOperands = currOperandList[i] - instructionByteCount(operands[1])
            if len(operands) == nOperands+1:
                breakBool = True
                break
            if len(operands) < nOperands+1:

                alwaysBigger = False
            if len(operands) > nOperands+1:
                alwaysSmaller = False
        if alwaysSmaller and not alwaysBigger:
            print("Error 005: Instrucción carece de operandos")
        if alwaysBigger and not alwaysSmaller:
            print("Error 006: Instrucción no lleva operandos")

        # Esto va si no concuerda con ningún tipo de direccionamiento
        print("Error 006: Instrucción no lleva operandos")


        
            



        
            
        




        

            


        #if (operands[0].lower() not in operandDict):
        #    continue
        print(operands)


           
            
        #print(line)
        """if line[0] == " " or line[0] =="*":
            print(line[0])
            continue"""

        #print(line.lstrip())








if __name__ == "__main__":
    """
    print("Validando operadores...")
    if RUTA == "":
        print("Error: No se ha especificado la ruta del archivo a compilar.")
    else:
        print(f"Archivo a compilar: {RUTA}")
        """

    #printFile()
    for line in lineas:
        print(line.split())
    #print(type(lineas[0]))
    