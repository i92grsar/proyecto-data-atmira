import pandas as pd

#Cargar los datos
df = pd.read_csv("data/messy_data.csv")

#Eliminar duplicados
df = df.drop_duplicates(subset="id", keep="first")

#Manejar valores nulos (reemplazar con "Desconocido" o un valor por defecto)
df["name"].fillna("Desconocido", inplace=True)
df["email"].fillna("no-email@example.com", inplace=True)
df["signup_date"].fillna("2000-01-01", inplace=True)

#Guardar el dataset limpio
df.to_csv("data/cleaned_data.csv", index=False)

print("✅ Dataset 'cleaned_data.csv' limpio y listo.")
