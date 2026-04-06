# Compilador MC62HC11

## Requisitos
- Los requisitos están en requirements.txt
- Para instalarlos (usando PIP) se recomienda usar
`pip install -r requirements.txt`
- Si se desea usar un ambiente virtual se recomienda usar
`python -m pip install -r requirements.txt`

## Para agregar librerías a requerimientos
### Usando pipreqs
- pipreqs es una librería que añade las versiones más recientes de paquetes importados 
- Esto según se encuentren en PyPI
- Se puede instalar con pip `pip install pipreqs`
- Para actualizar el archivo se usa `pipreqs --force` siendo esta última bandera necesaria para sobreescribir el archivo actual
### Usando pip freeze
- Se puede actualizar sin usar librerías 
- Agregará todos los paquetes instalados en el equipo, por lo tanto *se recomienda usar un ambiente virtual* 
- Sobreescribe el archivo `requirements.txt`
- Para usarse solo basta con ejecutar `pip freeze > requirements.txt"