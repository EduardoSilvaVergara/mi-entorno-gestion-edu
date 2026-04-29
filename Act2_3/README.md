# 📊 Pipeline de Datos – Validación estructural y semántica

## 📌 Descripción
Este proyecto implementa un pipeline de datos que incluye las etapas de:

- Ingesta de datos
- Limpieza y transformación
- Validación estructural
- Validación semántica

El objetivo es asegurar la calidad, integridad y consistencia de los datos antes de su uso en análisis o carga a base de datos.

---

## 📂 Dataset
El dataset utilizado es `ventas_sucias.csv`, el cual contiene datos con errores intencionales para validar el funcionamiento del pipeline.

Columnas:
- id
- nombre
- edad
- ciudad
- fecha_compra
- monto
- metodo_pago

---

## ⚙️ Etapas del Pipeline

### 1. Ingesta
Se cargan los datos desde un archivo CSV utilizando Pandas.

---

### 2. Limpieza y Transformación
Se aplican las siguientes transformaciones:
- Eliminación de espacios en texto
- Normalización de texto (minúsculas)
- Conversión de tipos de datos:
  - edad → numérico
  - monto → numérico
  - fecha_compra → datetime

---

### 3. Validación Estructural
Se verifica que los datos cumplan con requisitos técnicos:

Validaciones implementadas:
- Edad debe ser numérica
- Fecha debe ser válida
- Monto debe ser numérico
- Nombre no puede estar vacío

---

### 4. Validación Semántica
Se valida la lógica de negocio:

Validaciones implementadas:
- Edad debe estar entre 0 y 120
- Monto debe ser mayor a 0
- Método de pago debe ser válido (tarjeta, efectivo, transferencia)

---

## 📊 Resultados

El pipeline genera dos archivos:

- `ventas_limpias.csv` → datos válidos
- `ventas_errores.csv` → datos con errores estructurales y semánticos

Los errores se registran por fila, permitiendo trazabilidad.

---

## 🧠 Decisiones Técnicas

- Se separan validaciones estructurales y semánticas para mayor claridad
- No se modifica el dataset original
- Se utilizan funciones para modularizar el código
- Se consolidan todos los errores en un único archivo de salida
- Se utiliza Pandas por su eficiencia en procesamiento de datos

---

## ▶️ Ejecución en Google Colab

1. Subir el archivo `ventas_sucias.csv`
2. Ejecutar el notebook o script
3. Revisar los archivos generados

---

## 📦 Tecnologías utilizadas

- Python 3
- Pandas

---

## 📌 Autor
Proyecto académico – Pipeline de datos
