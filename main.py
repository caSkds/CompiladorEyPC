RUTA = "codigos_de_ejemplo/PRUEBA.ASC"

from OpcodeMatch import verifyMatch
from OperatorValidation import printFile
import memoryGeneration as mg
import colores as htmlGen


def main():
    try:
        with open(RUTA, "r"):
            pass
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo '{RUTA}'")
        return 

    print(f"Compilando: {RUTA}\n")

    _, erroresMatch, _ = verifyMatch(RUTA)
    erroresValidacion = printFile(RUTA)

    erroresCombinados = erroresMatch + erroresValidacion

    if erroresCombinados:
        print("  ERRORES DE COMPILACIÓN")
        for error in erroresCombinados:
            print(f"  {error}")
        print(f"\n{len(erroresCombinados)} error(es) encontrado(s).")
    else: 
        errores = mg.compileFile(RUTA)
        if errores:
            print("  ERRORES DE COMPILACIÓN")
            for error in errores:
                print(f"  {error}")
            print(f"\n{len(errores)} error(es) encontrado(s).")
            return
        
        print("Validación exitosa. Generando código máquina...\n")
        
        # Generador LST
        rutaLST = RUTA.rsplit(".", 1)[0] + ".LST"
        resultadoLST = mg.generateOutput(rutaLST, erroresCombinados)

        print(resultadoLST)
        print(f"\nArchivo generado: {rutaLST}")

        # Generador S19
        rutaS19 = RUTA.rsplit(".", 1)[0] + ".S19"
        resultadoS19 = mg.generateS19(rutaS19)

        print(f"Archivo generado: {rutaS19}")

        # Generador HTML (Colores)
        rutaHTML = RUTA.rsplit(".", 1)[0] + ".HTML"
        resultadoHTML = htmlGen.generateHTML(rutaHTML)
        print(f"Archivo generado: {rutaHTML}")


if __name__ == "__main__":
    main()