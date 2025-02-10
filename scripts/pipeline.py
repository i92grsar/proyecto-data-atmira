from prefect import flow, task
import subprocess
import psycopg2
import os

# Definir tareas
@task
def generate_dataset():
    subprocess.run(["python", "scripts/generate_messy_data.py"], check=True)

@task
def clean_dataset():
    subprocess.run(["python", "scripts/clean_messy_data.py"], check=True)

@task
def load_on_postgresql():
    conn = psycopg2.connect(
        dbname="postgresdb",
        user="postgres",
        password="postgres",
        host="postgres",
        port="5432"
    )
    cur = conn.cursor()
    
    cur.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            age INTEGER,
            signup_date DATE
        );
    """)
    conn.commit()
    
    cur.execute(f"TRUNCATE TABLE usuarios;")
    conn.commit()
    
    with open("data/cleaned_data.csv", "r") as f:
        next(f)  # Saltar la cabecera
        cur.copy_from(f, "usuarios", sep=",", columns=("id", "name", "email", "age", "signup_date"))
    
    conn.commit()
    cur.close()
    conn.close()

# Definir el flujo de Prefect
@flow
def pipeline_etl():
    generate_dataset()
    clean_dataset()
    load_on_postgresql()

# Ejecutar el flujo si se llama directamente
if __name__ == "__main__":
    pipeline_etl()
