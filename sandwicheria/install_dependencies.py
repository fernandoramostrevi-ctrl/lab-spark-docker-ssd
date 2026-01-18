import subprocess
import sys
import os
# Autor: Juan Gutierrez Miranda
# Fecha de creación: 2024-01-27
def install_requirements():
    # Verificar si requirements.txt existe
    if os.path.exists('requirements.txt'):
        # Instalar las dependencias
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])

if __name__ == '__main__':
    install_requirements()  # Instalar dependencias antes de iniciar la aplicación