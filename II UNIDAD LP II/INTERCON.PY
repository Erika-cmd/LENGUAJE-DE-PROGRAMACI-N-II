import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from scipy import stats
import numpy as np

# Estilo gráfico profesional
sns.set(style="whitegrid", palette="Set2")
plt.rcParams.update({'font.size': 11})

# Crear carpeta de salida
output_dir = "IMAGENES_INTERCON_COMPLETO"
os.makedirs(output_dir, exist_ok=True)

# Leer el dataset
df = pd.read_csv("DATASET_Talleres_Audiencias.csv", sep=";", encoding="latin1")
df["FECHA"] = pd.to_datetime(df["FECHA"], errors="coerce")
df.dropna(subset=["NUMERO_ASISTENTES", "NUMERO_PREGUNTAS", "NUMERO_HOMBRES", "NUMERO_MUJERES", "TIPO_EVENTO", "DEPARTAMENTO"], inplace=True)

# === IMAGEN 1: Cantidad de eventos por tipo ===
plt.figure(figsize=(8, 6))
ax = sns.countplot(data=df, x="TIPO_EVENTO", edgecolor="black")
plt.title("Figura 1. Distribución de eventos por tipo")
plt.xlabel("Tipo de Evento")
plt.ylabel("Cantidad de Eventos")
for p in ax.patches:
    ax.annotate(f'{p.get_height()}', (p.get_x() + p.get_width()/2, p.get_height()), ha='center', va='bottom')
plt.tight_layout()
plt.savefig(os.path.join(output_dir, "IMAGEN1.png"), dpi=300)
plt.close()

# === IMAGEN 2: Boxplot de asistentes por género ===
df_long = pd.melt(df, id_vars=["TIPO_EVENTO"], value_vars=["NUMERO_MUJERES", "NUMERO_HOMBRES"],
                  var_name="Género", value_name="Cantidad")
plt.figure(figsize=(8, 6))
sns.boxplot(data=df_long, x="Género", y="Cantidad", palette="pastel")
plt.title("Figura 2. Distribución del número de asistentes por género")
plt.xlabel("Género")
plt.ylabel("Cantidad de Asistentes")
plt.tight_layout()
plt.savefig(os.path.join(output_dir, "IMAGEN2.png"), dpi=300)
plt.close()

# === IMAGEN 3: Promedio de asistentes por tipo ===
promedios = df.groupby("TIPO_EVENTO")["NUMERO_ASISTENTES"].mean().reset_index()
plt.figure(figsize=(8, 6))
ax = sns.barplot(data=promedios, x="TIPO_EVENTO", y="NUMERO_ASISTENTES", edgecolor="black")
plt.title("Figura 3. Promedio de asistentes por tipo de evento")
plt.xlabel("Tipo de Evento")
plt.ylabel("Promedio de Asistentes")
for p in ax.patches:
    ax.annotate(f'{p.get_height():.1f}', (p.get_x() + p.get_width()/2, p.get_height()), ha='center', va='bottom')
plt.tight_layout()
plt.savefig(os.path.join(output_dir, "IMAGEN3.png"), dpi=300)
plt.close()

# === IMAGEN 4: Total de preguntas por tipo ===
preguntas = df.groupby("TIPO_EVENTO")["NUMERO_PREGUNTAS"].sum().reset_index()
plt.figure(figsize=(8, 6))
ax = sns.barplot(data=preguntas, x="TIPO_EVENTO", y="NUMERO_PREGUNTAS", palette="muted", edgecolor="black")
plt.title("Figura 4. Total de preguntas realizadas por tipo de evento")
plt.xlabel("Tipo de Evento")
plt.ylabel("Número de Preguntas")
for p in ax.patches:
    ax.annotate(f'{int(p.get_height())}', (p.get_x() + p.get_width()/2, p.get_height()), ha='center', va='bottom')
plt.tight_layout()
plt.savefig(os.path.join(output_dir, "IMAGEN4.png"), dpi=300)
plt.close()

# === IMAGEN 5: Evolución mensual ===
linea = df.groupby("FECHA").size().reset_index(name="Cantidad")
plt.figure(figsize=(10, 5))
sns.lineplot(data=linea, x="FECHA", y="Cantidad", marker="o", color="blue")
plt.title("Figura 5. Evolución mensual de eventos realizados")
plt.xlabel("Fecha")
plt.ylabel("Cantidad de Eventos")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(os.path.join(output_dir, "IMAGEN5.png"), dpi=300)
plt.close()

# === IMAGEN 6: Dispersión asistentes vs preguntas ===
plt.figure(figsize=(8, 6))
sns.scatterplot(data=df, x="NUMERO_ASISTENTES", y="NUMERO_PREGUNTAS", hue="TIPO_EVENTO", palette="Dark2")
plt.title("Figura 6. Relación entre asistentes y preguntas")
plt.xlabel("Número de Asistentes")
plt.ylabel("Número de Preguntas")
plt.tight_layout()
plt.savefig(os.path.join(output_dir, "IMAGEN6.png"), dpi=300)
plt.close()

# === IMAGEN 7: Eventos por departamento ===
departamentos = df["DEPARTAMENTO"].value_counts().reset_index()
departamentos.columns = ["DEPARTAMENTO", "Cantidad"]
plt.figure(figsize=(10, 6))
sns.barplot(data=departamentos, y="DEPARTAMENTO", x="Cantidad", palette="coolwarm", edgecolor="black")
plt.title("Figura 7. Distribución de eventos por departamento")
plt.xlabel("Cantidad de Eventos")
plt.ylabel("Departamento")
plt.tight_layout()
plt.savefig(os.path.join(output_dir, "IMAGEN7.png"), dpi=300)
plt.close()
# === IMAGEN 8: Regresión lineal asistentes → preguntas ===
plt.figure(figsize=(8, 6))
sns.regplot(data=df, x="NUMERO_ASISTENTES", y="NUMERO_PREGUNTAS", scatter_kws={"alpha": 0.5}, line_kws={"color": "red"})
plt.title("Figura 8. Regresión lineal: Asistentes vs. Preguntas")
plt.xlabel("Número de Asistentes")
plt.ylabel("Número de Preguntas")
slope, intercept, r_value, p_value, std_err = stats.linregress(df["NUMERO_ASISTENTES"], df["NUMERO_PREGUNTAS"])
plt.text(0.05, 0.95, f"y = {slope:.2f}x + {intercept:.2f}\nR² = {r_value**2:.2f}",
         transform=plt.gca().transAxes, fontsize=11, verticalalignment='top',
         bbox=dict(boxstyle='round', facecolor='white', alpha=0.5))
plt.tight_layout()
plt.savefig(os.path.join(output_dir, "IMAGEN8.png"), dpi=300)
plt.close()

# === IMAGEN 9: Participación femenina por departamento ===
fem_dep = df.groupby("DEPARTAMENTO")["NUMERO_MUJERES"].sum().sort_values(ascending=False).reset_index()
plt.figure(figsize=(10, 6))
sns.barplot(data=fem_dep, y="DEPARTAMENTO", x="NUMERO_MUJERES", palette="mako")
plt.title("Figura 9. Participación femenina total por departamento")
plt.xlabel("Total de Mujeres")
plt.ylabel("Departamento")
plt.tight_layout()
plt.savefig(os.path.join(output_dir, "IMAGEN9.png"), dpi=300)
plt.close()

# === IMAGEN 10: ANOVA por tipo de evento ===
talleres = df[df["TIPO_EVENTO"] == "Taller"]["NUMERO_ASISTENTES"]
audiencias = df[df["TIPO_EVENTO"] == "Audiencia Pública"]["NUMERO_ASISTENTES"]
anova_result = stats.f_oneway(talleres, audiencias)
plt.figure(figsize=(6, 4))
plt.axis("off")
plt.text(0, 0.5, f"Figura 10. ANOVA - Asistentes por tipo de evento\n\n"
                 f"F = {anova_result.statistic:.2f}\n"
                 f"p = {anova_result.pvalue:.4f}",
         fontsize=12, bbox=dict(boxstyle="round", facecolor="lightgrey", alpha=0.7))
plt.tight_layout()
plt.savefig(os.path.join(output_dir, "IMAGEN10.png"), dpi=300)
plt.close()

# === IMAGEN 11: Test t hombres vs mujeres ===
t_test = stats.ttest_ind(df["NUMERO_HOMBRES"], df["NUMERO_MUJERES"], equal_var=False)
plt.figure(figsize=(6, 4))
plt.axis("off")
plt.text(0, 0.5, f"Figura 11. Test t - Hombres vs. Mujeres\n\n"
                 f"t = {t_test.statistic:.2f}\n"
                 f"p = {t_test.pvalue:.4f}",
         fontsize=12, bbox=dict(boxstyle="round", facecolor="lightyellow", alpha=0.8))
plt.tight_layout()
plt.savefig(os.path.join(output_dir, "IMAGEN11.png"), dpi=300)
plt.close()

# === IMAGEN 12: Correlación Hombres vs Mujeres ===
correlation = stats.pearsonr(df["NUMERO_HOMBRES"], df["NUMERO_MUJERES"])
plt.figure(figsize=(8, 6))
sns.scatterplot(x=df["NUMERO_HOMBRES"], y=df["NUMERO_MUJERES"], alpha=0.5)
sns.regplot(x=df["NUMERO_HOMBRES"], y=df["NUMERO_MUJERES"], scatter=False, color="red")
plt.title("Figura 12. Correlación: Hombres vs. Mujeres")
plt.xlabel("Número de Hombres")
plt.ylabel("Número de Mujeres")
plt.text(0.05, 0.95, f"r = {correlation[0]:.2f}\np = {correlation[1]:.4f}",
         transform=plt.gca().transAxes, fontsize=11, verticalalignment='top',
         bbox=dict(boxstyle='round', facecolor='white', alpha=0.5))
plt.tight_layout()
plt.savefig(os.path.join(output_dir, "IMAGEN12.png"), dpi=300)
plt.close()

# === IMAGEN 13: Mapa de calor (heatmap) ===
plt.figure(figsize=(10, 6))
corr = df[["NUMERO_HOMBRES", "NUMERO_MUJERES", "NUMERO_ASISTENTES", "NUMERO_PREGUNTAS"]].corr()
sns.heatmap(corr, annot=True, cmap="coolwarm", vmin=-1, vmax=1)
plt.title("Figura 13. Mapa de calor de correlaciones")
plt.tight_layout()
plt.savefig(os.path.join(output_dir, "IMAGEN13.png"), dpi=300)
plt.close()

# === IMAGEN 14: Violinplot género vs tipo de evento ===
df_violin = pd.melt(df, id_vars=["TIPO_EVENTO"], value_vars=["NUMERO_HOMBRES", "NUMERO_MUJERES"],
                    var_name="Género", value_name="Cantidad")
plt.figure(figsize=(9, 6))
sns.violinplot(data=df_violin, x="TIPO_EVENTO", y="Cantidad", hue="Género", split=True, palette="muted")
plt.title("Figura 14. Distribución de asistentes por género y tipo de evento")
plt.xlabel("Tipo de Evento")
plt.ylabel("Cantidad de Asistentes")
plt.tight_layout()
plt.savefig(os.path.join(output_dir, "IMAGEN14.png"), dpi=300)
plt.close()
# === IMAGEN 15: Tabla resumen estadística como imagen ===
summary = df[["NUMERO_HOMBRES", "NUMERO_MUJERES", "NUMERO_ASISTENTES", "NUMERO_PREGUNTAS"]].describe().T
plt.figure(figsize=(10, 3))
plt.axis('off')
table = plt.table(cellText=np.round(summary.values, 2),
                  colLabels=summary.columns,
                  rowLabels=summary.index,
                  cellLoc='center', loc='center')
table.scale(1.2, 1.2)
plt.title("Figura 15. Estadísticas descriptivas de variables numéricas")
plt.savefig(os.path.join(output_dir, "IMAGEN15.png"), dpi=300)
plt.close()

# === IMAGEN 16: Tabla resumen de resultados estadísticos ===
plt.figure(figsize=(8, 3))
plt.axis('off')
stats_data = [
    ["ANOVA F", f"{anova_result.statistic:.2f}"],
    ["ANOVA p", f"{anova_result.pvalue:.4f}"],
    ["Test t", f"{t_test.statistic:.2f}"],
    ["Test t p", f"{t_test.pvalue:.4f}"],
    ["Correlación r", f"{correlation[0]:.2f}"],
    ["Correlación p", f"{correlation[1]:.4f}"],
    ["Regresión R²", f"{r_value**2:.2f}"],
    ["Ecuación", f"y = {slope:.2f}x + {intercept:.2f}"]
]
table = plt.table(cellText=stats_data, colLabels=["Estadístico", "Valor"],
                  cellLoc='center', loc='center')
table.scale(1.2, 1.4)
plt.title("Figura 16. Resumen de resultados estadísticos")
plt.tight_layout()
plt.savefig(os.path.join(output_dir, "IMAGEN16.png"), dpi=300)
plt.close()

# === IMAGEN 17: Pirámide de género por tipo de evento ===
pivot = df.groupby("TIPO_EVENTO")[["NUMERO_HOMBRES", "NUMERO_MUJERES"]].sum()
pivot["NUMERO_HOMBRES"] *= -1
plt.figure(figsize=(9, 5))
plt.barh(pivot.index, pivot["NUMERO_HOMBRES"], color="skyblue", label="Hombres")
plt.barh(pivot.index, pivot["NUMERO_MUJERES"], color="lightpink", label="Mujeres")
plt.title("Figura 17. Pirámide de género por tipo de evento")
plt.xlabel("Cantidad de Asistentes (negativo = hombres)")
plt.legend()
plt.tight_layout()
plt.savefig(os.path.join(output_dir, "IMAGEN17.png"), dpi=300)
plt.close()

# === IMAGEN 18: Participación mensual por tipo de evento (stacked) ===
df['MES'] = df['FECHA'].dt.to_period('M')
stacked = df.groupby(['MES', 'TIPO_EVENTO']).size().unstack(fill_value=0)
stacked.index = stacked.index.astype(str)
stacked.plot(kind='bar', stacked=True, figsize=(12, 6), colormap='Set2')
plt.title("Figura 18. Participación mensual por tipo de evento")
plt.xlabel("Mes")
plt.ylabel("Número de Eventos")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(os.path.join(output_dir, "IMAGEN18.png"), dpi=300)
plt.close()
