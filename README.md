# Workflow Managers: Price Tracker

Este proyecto utiliza **Prefect** para crear un flujo de trabajo que rastrea los precios de productos en línea y guarda su historial. Actualmente funciona con **Mercado Libre México**.

---

## Funcionalidades

- Descargar la página del producto.
- Extraer el precio actual del artículo.
- Guardar el precio con la fecha y hora en un archivo CSV.
- Permite analizar la evolución del precio a lo largo del tiempo para determinar cuándo estuvo más barato.

---

## Tecnologías utilizadas

- **Python 3.13**
- **Prefect** (para la orquestación del flujo)
- **Requests** (para obtener el HTML del producto)
- **BeautifulSoup4** (para parsear el HTML)
- **CSV** (para almacenar el historial de precios)

---

## Instalación

1. Clona el repositorio:

bash
git clone https://github.com/diegohdz17/Workflow-managers.git
cd Workflow-managers

2.Crea un entorno virtual (opcional pero recomendado):

python -m venv venv
source venv/Scripts/activate  # Window

3. Instala las dependencias:
pip install prefect requests beautifulsoup4

Uso

Edita el archivo precios.py para cambiar la URL del producto que deseas rastrear.

Ejecuta el flujo:
python precios.py
Cada ejecución guardará un registro del precio actual en el archivo precios.csv

Notas

Amazon y otras tiendas suelen proteger su contenido, por lo que es más fácil hacer scraping en páginas como Mercado Libre.

El flujo se puede programar con Prefect o con un programador de tareas (cron) para obtener precios de manera periódica.

Resultado del csv


<img width="549" height="274" alt="Captura1" src="https://github.com/user-attachments/assets/1ca79a32-5efd-4580-b571-3bd29dffde3f" />



