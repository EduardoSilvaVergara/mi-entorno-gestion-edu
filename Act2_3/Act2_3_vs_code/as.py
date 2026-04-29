# =========================
# 1. INGESTA
# =========================
import pandas as pd

df = pd.read_csv("ventas_sucias.csv")

print("Datos originales:")
print(df)


# =========================
# 2. LIMPIEZA Y TRANSFORMACIÓN
# =========================

df['nombre'] = df['nombre'].str.strip()
df['ciudad'] = df['ciudad'].str.strip()
df['metodo_pago'] = df['metodo_pago'].str.strip().str.lower()

df['edad'] = pd.to_numeric(df['edad'], errors='coerce')
df['monto'] = pd.to_numeric(df['monto'], errors='coerce')
df['fecha_compra'] = pd.to_datetime(df['fecha_compra'], errors='coerce')

print("\nDatos después de limpieza:")
print(df)


# =========================
# 3. VALIDACIÓN ESTRUCTURAL
# =========================

def validar_estructura(row):
    errores = []

    if pd.isna(row['edad']):
        errores.append("Edad no es numérica")

    if pd.isna(row['fecha_compra']):
        errores.append("Fecha inválida")

    if pd.isna(row['monto']):
        errores.append("Monto no numérico")

    if pd.isna(row['nombre']) or str(row['nombre']).strip() == "":
        errores.append("Nombre vacío")

    return errores


df['errores_estructurales'] = df.apply(validar_estructura, axis=1)

# Separar datos
df_struct_ok = df[df['errores_estructurales'].apply(len) == 0].copy()
df_struct_error = df[df['errores_estructurales'].apply(len) > 0].copy()


# =========================
# 3.1 VALIDACIÓN DE DUPLICADOS (ID)
# =========================

# Detectar duplicados
duplicados = df_struct_ok[df_struct_ok.duplicated(subset=['id'], keep=False)]

# Marcar error en duplicados
df_struct_ok.loc[df_struct_ok['id'].isin(duplicados['id']), 'errores_estructurales'] = \
    df_struct_ok['errores_estructurales'].apply(lambda x: x + ["ID duplicado"])

# Re-separar después de agregar error
df_struct_error = pd.concat([
    df_struct_error,
    df_struct_ok[df_struct_ok['errores_estructurales'].apply(len) > 0]
], ignore_index=True)

df_struct_ok = df_struct_ok[df_struct_ok['errores_estructurales'].apply(len) == 0]

print("\nErrores estructurales:")
print(df_struct_error[['id', 'errores_estructurales']])


# =========================
# 4. VALIDACIÓN SEMÁNTICA
# =========================

def validar_semantica(row):
    errores = []

    if row['edad'] < 0 or row['edad'] > 120:
        errores.append("Edad fuera de rango")

    if row['monto'] <= 0:
        errores.append("Monto debe ser positivo")

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

# Marcar tipo de error (extra pro)
df_struct_error['tipo_error'] = 'estructural'
df_final_error['tipo_error'] = 'semantico'

# Unificar errores
df_errores = pd.concat([df_struct_error, df_final_error], ignore_index=True)

print("\nDatos con errores:")
print(df_errores)

# Guardar resultados
df_final_ok.to_csv("ventas_limpias.csv", index=False)
df_errores.to_csv("ventas_errores.csv", index=False)