from main import RUTA

file = open(RUTA, "r")
lineas = file.readlines()




if __name__ == "__main__":
    print("Validando operadores...")
    if RUTA == "":
        print("Error: No se ha especificado la ruta del archivo a compilar.")
    else:
        print(f"Archivo a compilar: {RUTA}")