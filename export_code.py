import os

# Ruta del directorio raíz de tu proyecto Django
project_directory = os.path.dirname(os.path.abspath(__file__))

# Función para exportar el código de un archivo a un archivo de texto unificado
def export_code(file_path, output_file):
    with open(file_path, 'r', encoding='utf-8') as file:
        code = file.read()
        output_file.write(f'\n\n/* {file_path} */\n\n{code}')

# Archivo de salida unificado
output_file_path = os.path.join(project_directory, 'unified-code.txt')

# Función para buscar y exportar archivos en un directorio y sus subdirectorios
def export_files_in_directory(directory_path, output_file, file_extensions):
    for root, _, files in os.walk(directory_path):
        for file in files:
            if file.endswith(tuple(file_extensions)):
                file_path = os.path.join(root, file)
                export_code(file_path, output_file)

# Lista de extensiones de archivo a exportar
file_extensions_to_export = ['.py', '.html', '.css']

# Inicia el proceso de exportación desde la carpeta "idea_app"
with open(output_file_path, 'w', encoding='utf-8') as output_file:
    export_files_in_directory(project_directory, output_file, file_extensions_to_export)

# También exporta los archivos de la carpeta "myproject"
myproject_directory = os.path.join(project_directory, 'myproject')
with open(output_file_path, 'a', encoding='utf-8') as output_file:
    export_files_in_directory(myproject_directory, output_file, file_extensions_to_export)

print(f'Código exportado exitosamente a {output_file_path}')
