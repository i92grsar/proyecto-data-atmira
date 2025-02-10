Autor: Rafael Grande Salido

INTRODUCCIÓN:

Este proyecto demuestra un pipeline de datos completo que genera datos sintéticos "messy", los limpia y los carga en una base de datos PostgreSQL. La orquestación del proceso se realiza mediante Prefect y todo el entorno se ejecuta en contenedores Docker, coordinados con Docker Compose.

-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

¿CÓMO FUNCIONA EL PIPELINE?

    Generación del Dataset:
Se ejecuta scripts/generate_messy_data.py para crear un archivo CSV llamado messy_data.csv con aproximadamente 5000 registros que incluyen errores intencionales (duplicados, valores nulos y errores tipográficos).

    Limpieza del Dataset:
Se ejecuta scripts/clean_messy_data.py para procesar messy_data.csv: elimina duplicados, gestiona valores nulos (rellenándolos con valores por defecto) y corrige errores. El resultado se guarda en data/cleaned_data.csv.

    Carga en PostgreSQL:
El pipeline orquestado en scripts/pipeline.py (usando Prefect) ejecuta las tareas de generación y limpieza, luego se conecta a la base de datos PostgreSQL para:
	- Crear la tabla usuarios si no existe.
	- Truncar la tabla (para evitar duplicados).
	- Cargar los datos del CSV (data/cleaned_data.csv) en la tabla.

-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

CONTENERIZACIÓN U ORQUESTACIÓN

El proyecto se ejecuta completamente en contenedores Docker:

    PostgreSQL: Se levanta mediante Docker Compose.
    Pipeline (Prefect): Se construye con un Dockerfile que instala las dependencias y ejecuta el pipeline automáticamente.

El archivo docker-compose.yml define dos servicios:

    postgres: Servicio de base de datos.
    pipeline: Servicio que construye y ejecuta el pipeline ETL.

-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

INSTRUCCIONES PARA EJECUTAR EL PROYECTO

    1. Requisitos Previos:
	- Docker y Docker Compose instalados en el sistema.
        - Clonar el repositorio del proyecto.

    2. Construir y Levantar los Servicios:
En la raíz del proyecto, abre una terminal y ejecuta:

		docker-compose up --build

Este comando construirá la imagen del pipeline, levantará el contenedor de PostgreSQL y ejecutará el pipeline ETL automáticamente.

     3. Verificar la Ejecución:
El pipeline generará los archivos messy_data.csv y data/cleaned_data.csv.

Puedes conectarte al contenedor de PostgreSQL para verificar que la tabla usuarios se haya creado y que los datos se hayan insertado:

	docker exec -it postgres_container psql -U postgres -d postgresdb

Luego, en el prompt de PostgreSQL:

	\dt
	SELECT * FROM usuarios LIMIT 10;

-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

PROBLEMAS ENCONTRADOS Y SOLUCIONES:

	Problemas de Instalación de Dependencias:
Se encontraron errores al instalar paquetes como psycopg2 (solucionado utilizando psycopg2-binary) y otros que requerían herramientas como Rust. Se resolvieron instalando las versiones binarias y ajustando el entorno.


Al insertar datos manualmente con COPY, surgió un error porque el id en la línea 5002 estaba duplicado. Se esperaba un máximo de 5001 líneas, pero a partir de la 5002 todos los id se repetían.

El error ocurrió porque en el código se generaban duplicados y luego se les añadían errores. Al limpiar los datos, drop_duplicates() no eliminaba estos registros, ya que detecta duplicados solo si toda la fila es idéntica, pero los valores modificados impedían su detección.

Se corrigió este error usando:

df = df.drop_duplicates(subset="id", keep="first")

Esto garantizó que los duplicados se eliminaran basándose solo en el id, evitando errores al insertar en la base de datos.

Luego se han tenido otros errores menores como fallos tipográficos, errores en rutas, y en el nombramiento de archivos, variables, etc.