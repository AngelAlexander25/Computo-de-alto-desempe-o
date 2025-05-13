#!/bin/bash
# Script para preparar y subir el dashboard Messi a GitHub Pages

# Colores para mensajes
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}=========================================${NC}"
echo -e "${BLUE}   Preparando Dashboard Messi para GitHub Pages   ${NC}"
echo -e "${BLUE}=========================================${NC}"

# Verificar si git está instalado
if ! command -v git &> /dev/null; then
    echo -e "${RED}Error: Git no está instalado. Por favor instala Git primero.${NC}"
    exit 1
fi

# Verificar si Python está instalado
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Error: Python 3 no está instalado. Es necesario para convertir el CSV a JSON.${NC}"
    exit 1
fi

# Verificar si pandas está instalado
python3 -c "import pandas" 2>/dev/null
if [ $? -ne 0 ]; then
    echo -e "${BLUE}Instalando pandas...${NC}"
    pip install pandas
    if [ $? -ne 0 ]; then
        echo -e "${RED}Error al instalar pandas. Por favor instálalo manualmente: pip install pandas${NC}"
        exit 1
    fi
fi

# Verificar que exista el archivo CSV
if [ ! -f "messi_barca.csv" ]; then
    echo -e "${RED}Error: No se encuentra el archivo messi_barca.csv en el directorio actual.${NC}"
    echo -e "${RED}Por favor, asegúrate de que el archivo CSV está en este directorio.${NC}"
    exit 1
fi

# Verificar que existan los archivos HTML y el script Python
if [ ! -f "index.html" ]; then
    echo -e "${RED}Error: No se encuentra el archivo index.html en el directorio actual.${NC}"
    echo -e "${RED}Por favor, renombra el archivo HTML del dashboard como index.html${NC}"
    exit 1
fi

if [ ! -f "convert_csv_to_json.py" ]; then
    echo -e "${RED}Error: No se encuentra el script convert_csv_to_json.py${NC}"
    echo -e "${RED}Por favor, asegúrate de tener este archivo en el directorio actual.${NC}"
    exit 1
fi

# Ejecutar el script Python para convertir CSV a JSON
echo -e "${BLUE}Convirtiendo CSV a JSON...${NC}"
python3 convert_csv_to_json.py

if [ ! -f "messi_data.json" ]; then
    echo -e "${RED}Error: No se pudo generar el archivo JSON correctamente.${NC}"
    exit 1
fi

echo -e "${GREEN}✓ JSON generado correctamente${NC}"

# Preguntar el nombre del repositorio de GitHub
echo -e "${BLUE}Por favor, introduce el nombre de tu repositorio de GitHub (sin el nombre de usuario):${NC}"
read REPO_NAME

# Preguntar el nombre de usuario de GitHub
echo -e "${BLUE}Por favor, introduce tu nombre de usuario de GitHub:${NC}"
read GITHUB_USER

# Crear directorio temporal para la subida
TEMP_DIR="temp_gh_pages"
echo -e "${BLUE}Creando directorio temporal para GitHub Pages...${NC}"
mkdir -p $TEMP_DIR

# Copiar archivos necesarios
cp index.html $TEMP_DIR/
cp messi_data.json $TEMP_DIR/

# Inicializar repositorio Git en el directorio temporal
cd $TEMP_DIR
git init
git add .
git commit -m "Initial commit for Messi Dashboard"

# Crear rama gh-pages
git branch -M gh-pages

# Añadir repositorio remoto
git remote add origin https://github.com/$GITHUB_USER/$REPO_NAME.git

# Preguntar si el repositorio ya existe
echo -e "${BLUE}¿El repositorio $REPO_NAME ya existe en tu cuenta de GitHub? (s/n)${NC}"
read REPO_EXISTS

if [ "$REPO_EXISTS" = "n" ]; then
    echo -e "${BLUE}Por favor, crea el repositorio $REPO_NAME en tu cuenta de GitHub antes de continuar.${NC}"
    echo -e "${BLUE}Ve a https://github.com/new y crea un repositorio público con el nombre $REPO_NAME${NC}"
    echo -e "${BLUE}Presiona Enter cuando hayas creado el repositorio...${NC}"
    read
fi

# Subir al repositorio
echo -e "${BLUE}Subiendo archivos a GitHub Pages...${NC}"
git push -f origin gh-pages

if [ $? -eq 0 ]; then
    echo -e "${GREEN}¡Felicidades! Tu dashboard ha sido subido exitosamente a GitHub Pages.${NC}"
    echo -e "${GREEN}Podrás acceder a él en: https://$GITHUB_USER.github.io/$REPO_NAME/${NC}"
    echo -e "${GREEN}Puede tardar unos minutos en estar disponible.${NC}"
else
    echo -e "${RED}Hubo un problema al subir a GitHub. Por favor, verifica tus credenciales e intenta de nuevo.${NC}"
fi

# Limpiar
cd ..
echo -e "${BLUE}¿Deseas eliminar el directorio temporal? (s/n)${NC}"
read CLEAN_UP

if [ "$CLEAN_UP" = "s" ]; then
    rm -rf $TEMP_DIR
    echo -e "${GREEN}Directorio temporal eliminado.${NC}"
fi

echo -e "${GREEN}¡Proceso completado!${NC}"