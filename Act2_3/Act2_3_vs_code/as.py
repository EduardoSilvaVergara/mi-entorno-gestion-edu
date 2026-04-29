# =========================
# 1. INGESTA
# =========================
import pandas as pd
import re

# Cargar datos
df = pd.read_csv("ventas_sucias.csv")

print("Datos originales:")
print(df)


# =========================
# 2. LIMPIEZA Y TRANSFORMACIÓN
# =========================

# Eliminar espacios en texto
df['nombre'] = df['nombre'].str.strip()
df['ciudad'] = df['ciudad'].str.strip()
df['metodo_pago'] = df['metodo_pago'].str.strip().str.lower()

# Convertir tipos
df['edad'] = pd.to_numeric(df['edad'], errors='coerce')
df['monto'] = pd.to_numeric(df['monto'], errors='coerce')
df['fecha_compra'] = pd.to_datetime(df['fecha_compra'], errors='coerce')

print("\nDatos después de limpieza:")
print(df)


# =========================
# 3. VALIDACIÓN ESTRUCTURAL
# =========================

errores_estructurales = []

def validar_estructura(row):
    errores = []

    # 1. Edad válida (número)
    if pd.isna(row['edad']):
        errores.append("Edad no es numérica")

    # 2. Fecha válida
    if pd.isna(row['fecha_compra']):
        errores.append("Fecha inválida")

    # 3. Monto válido
    if pd.isna(row['monto']):
        errores.append("Monto no numérico")

    # 4. Nombre no vacío
    if pd.isna(row['nombre']) or str(row['nombre']).strip() == "":
        errores.append("Nombre vacío")

    return errores


df['errores_estructurales'] = df.apply(validar_estructura, axis=1)

# Separar datos
df_struct_ok = df[df['errores_estructurales'].apply(len) == 0].copy()
df_struct_error = df[df['errores_estructurales'].apply(len) > 0].copy()

print("\nErrores estructurales:")
print(df_struct_error[['id', 'errores_estructurales']])


# =========================
# 4. VALIDACIÓN SEMÁNTICA
# =========================

def validar_semantica(row):
    errores = []

    # 1. Edad lógica (0 - 120)
    if row['edad'] < 0 or row['edad'] > 120:
        errores.append("Edad fuera de rango")

    # 2. Monto positivo
    if row['monto'] <= 0:
        errores.append("Monto debe ser positivo")

    # 3. Método de pago válido
    metodos_validos = ['tarjeta', 'efectivo', 'transferencia']
    if row['metodo_pago'] not in metodos_validos:
        errores.append("Método de pago inválido")

    return errores


df_struct_ok['errores_semanticos'] = df_struct_ok.apply(validar_semantica, axis=1)

# Separar datos finales
df_final_ok = df_struct_ok[df_struct_ok['errores_semanticos'].apply(len) == 0]
df_final_error = df_struct_ok[df_struct_ok['errores_semanticos'].apply(len) > 0]

print("\nErrores semánticos:")
print(df_final_error[['id', 'errores_semanticos']])


# =========================
# 5. RESULTADOS FINALES
# =========================

print("\nDatos válidos finales:")
print(df_final_ok)

# Unificar TODOS los errores
df_errores = pd.concat([df_struct_error, df_final_error], ignore_index=True)

print("\nDatos con errores:")
print(df_errores)

# Guardar resultados
df_final_ok.to_csv("ventas_limpias.csv", index=False)
df_errores.to_csv("ventas_errores.csv", index=False)