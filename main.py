RUTA = "codigos_de_ejemplo/EXEMPLO.ASC"

from OpcodeMatch import verifyMatch
from OperatorValidation import printFile
import memoryGeneration as mg


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
        print(f"\n{len(erroresCombinados)} error(es) encontrado(s). Compilación abortada.")
    else: 
        print("Validación exitosa. Generando código máquina...\n")

        mg.compileFile(RUTA)

        rutaSalida = RUTA.rsplit(".", 1)[0] + ".LST"

        resultado = mg.generateOutput(rutaSalida)

        print(resultado)
        print(f"\nArchivo generado: {rutaSalida}")


if __name__ == "__main__":
    main()