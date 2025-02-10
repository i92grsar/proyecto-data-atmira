import pandas as pd
import numpy as np
import random
import uuid
from faker import Faker

# Inicializar Faker para generar datos aleatorios
fake = Faker()

# Parámetros
num_records = 5000  # Número de registros
error_percentage = 0.02  # 2% de errores

#Generar datos limpios
data = []
for _ in range(num_records):
    data.append({
        "id": str(uuid.uuid4()),  # Generar UUID
        "name": fake.name(),
        "email": fake.email(),
        "age": random.randint(18, 80),
        "signup_date": fake.date_between(start_date="-5y", end_date="today").strftime("%Y-%m-%d")
    })

df = pd.DataFrame(data)

#Introducir duplicados (2% de los registros)
num_duplicates = int(num_records * error_percentage)
duplicates = df.sample(n=num_duplicates, replace=True)  # Seleccionar aleatoriamente registros duplicados
df = pd.concat([df, duplicates], ignore_index=True)

#Introducir valores nulos en name, email y signup_date (2% de los registros)
for col in ["name", "email", "signup_date"]:
    df.loc[df.sample(frac=error_percentage).index, col] = np.nan

#Introducir errores tipográficos en name y email (2% de los registros)
def introduce_typo(value):
    if isinstance(value, str) and len(value) > 3:
        pos = random.randint(0, len(value) - 2)
        return value[:pos] + value[pos+1] + value[pos] + value[pos+2:]
    return value

for col in ["name", "email"]:
    typo_indices = df.sample(frac=error_percentage).index
    df.loc[typo_indices, col] = df.loc[typo_indices, col].apply(introduce_typo)

#Guardar en CSV
df.to_csv("data/messy_data.csv", index=False)
print("✅ Dataset 'messy_data.csv' generado con éxito.")
