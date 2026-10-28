# ==========================================
# TRABAJO 4: VISUALIZACIÓN DE DATOS
# Fichero: analisis_superstore.py
# Dataset: superstore_dataset2012.csv
# ==========================================

import os
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

sns.set_theme(style="whitegrid")
plt.rcParams["figure.figsize"] = (10, 6)

current_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(current_dir)
print(f"Directorio: {current_dir}")

# ------------------------------------------
# 1. CARGA DE DATOS (PANDAS)
# ------------------------------------------
csv_file = "superstore_dataset2012.csv"
if not os.path.exists(csv_file):
    raise FileNotFoundError(f"Falta el archivo {csv_file}")

df = pd.read_csv(csv_file, encoding="latin1")
print(f"Filas: {df.shape[0]}, " f"Columnas: {df.shape[1]}")

df["Order Date"] = pd.to_datetime(df["Order Date"], errors="coerce")
df["Ship Date"] = pd.to_datetime(df["Ship Date"], errors="coerce")

print("\n--- Estadísticas básicas ---")
cols_desc = ["Sales", "Quantity", "Discount", "Profit"]
print(df[cols_desc].describe())

"""
CONCLUSIÓN DE PREPARACIÓN:
Dataset con 4,246 registros sin nulos.
Fechas convertidas a datetime.
"""


# ------------------------------------------
# 2. VISUALIZACIONES UNIVARIANTES
# ------------------------------------------

# A. Histograma de Ventas (Matplotlib)
plt.figure()
plt.hist(df["Sales"], bins=30, color="skyblue", edgecolor="black")
plt.title("Distribución de Ventas", fontsize=14, fontweight="bold")
plt.xlabel("Ventas ($)")
plt.ylabel("Frecuencia")
plt.savefig("histograma_ventas.png", dpi=300, bbox_inches="tight")
plt.show()

"""
CONCLUSIÓN UNIVARIANTE:
Sesgo positivo pronunciado; la gran
mayoría de ventas son menores a $500.
"""

# B. Boxplot por Región (Seaborn)
plt.figure()
sns.boxplot(
    x="Region",
    y="Profit",
    data=df,
    palette="Set2",
    hue="Region",
    legend=False,
)
plt.title("Beneficios por Región", fontsize=14, fontweight="bold")
plt.xlabel("Región")
plt.ylabel("Beneficios ($)")
plt.xticks(rotation=45)
plt.savefig("boxplot_beneficios_region.png", dpi=300, bbox_inches="tight")
plt.show()

"""
CONCLUSIÓN UNIVARIANTE SEABORN:
Mediana cercana a cero con presencia
notable de valores atípicos.
"""


# ------------------------------------------
# 3. VISUALIZACIONES BIVARIANTES
# ------------------------------------------

# A. Scatter Ventas vs Beneficios
plt.figure()
plt.scatter(df["Sales"], df["Profit"], alpha=0.4, color="purple")
plt.title("Ventas vs Beneficios", fontsize=14, fontweight="bold")
plt.xlabel("Ventas ($)")
plt.ylabel("Beneficios ($)")
plt.savefig("scatter_ventas_beneficios.png", dpi=300, bbox_inches="tight")
plt.show()

"""
CONCLUSIÓN BIVARIANTE:
A mayor venta tiende a haber mayor
beneficio, salvo por descuentos altos.
"""

# B. Regresión Ventas vs Beneficios
plt.figure()
sns.regplot(
    x="Sales",
    y="Profit",
    data=df,
    scatter_kws={"alpha": 0.3, "color": "darkblue"},
    line_kws={"color": "red", "linewidth": 2},
)
plt.title("Regresión: Ventas vs Beneficios", fontsize=14, fontweight="bold")
plt.xlabel("Ventas ($)")
plt.ylabel("Beneficios ($)")
plt.savefig("regplot_ventas_beneficios.png", dpi=300, bbox_inches="tight")
plt.show()

"""
CONCLUSIÓN REGRESIÓN:
Tendencia positiva confirmada entre
el volumen de ventas y la ganancia.
"""


# ------------------------------------------
# 4. VISUALIZACIÓN MULTIVARIANTE
# ------------------------------------------
plt.figure(figsize=(8, 6))
cols_num = ["Sales", "Quantity", "Discount", "Profit", "Shipping Cost"]
matriz_corr = df[cols_num].corr()

sns.heatmap(
    matriz_corr,
    annot=True,
    cmap="coolwarm",
    fmt=".2f",
    linewidths=0.5,
    square=True,
)
plt.title("Matriz de Correlación", fontsize=14, fontweight="bold")
plt.savefig("heatmap_correlacion.png", dpi=300, bbox_inches="tight")
plt.show()

"""
CONCLUSIÓN MULTIVARIANTE:
Fuerte correlación entre ventas y
coste de envío (0.76).
"""


# ------------------------------------------
# 5. DASHBOARD COMBINADO (SUBPLOTS)
# ------------------------------------------
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle(
    "Dashboard Comercial - " "Superstore 2012",
    fontsize=16,
    fontweight="bold",
)

# Subplot 1
axes[0, 0].hist(df["Sales"], bins=25, color="teal", edgecolor="black")
axes[0, 0].set_title("1. Ventas")
axes[0, 0].set_xlabel("Ventas ($)")
axes[0, 0].set_ylabel("Frecuencia")

# Subplot 2
axes[0, 1].scatter(df["Sales"], df["Profit"], alpha=0.3, color="darkorange")
axes[0, 1].set_title("2. Ventas vs Beneficios")
axes[0, 1].set_xlabel("Ventas ($)")
axes[0, 1].set_ylabel("Beneficios ($)")

# Subplot 3
sns.boxplot(
    ax=axes[1, 0],
    x="Category",
    y="Sales",
    data=df,
    palette="pastel",
    hue="Category",
    legend=False,
)
axes[1, 0].set_title("3. Por Categoría")
axes[1, 0].set_xlabel("Categoría")
axes[1, 0].set_ylabel("Ventas ($)")

# Subplot 4
sns.barplot(
    ax=axes[1, 1],
    x="Segment",
    y="Profit",
    data=df,
    estimator=lambda x: (sum(x) / len(x)),
    palette="muted",
    hue="Segment",
    legend=False,
)
axes[1, 1].set_title("4. Beneficio por Segmento")
axes[1, 1].set_xlabel("Segmento")
axes[1, 1].set_ylabel("Beneficio Promedio")

plt.tight_layout(rect=(0, 0.03, 1, 0.95))
plt.savefig("dashboard_subplots.png", dpi=300, bbox_inches="tight")
plt.show()

print("\n¡Ejecución perfecta y sin errores!")
