import streamlit as st
import pandas as pd
import plotly.express as px
from scipy.stats import chi2_contingency, ttest_ind

# Función para Chi2
def chi2_test(df, target_col='target', alpha=0.05):
    resultados = []
    
    # Definir qué columnas son numéricas continuas para discretizar
    num_cols = df.select_dtypes(include=['float64','int64']).columns.drop(target_col)
    
    # Discretizar variables continuas
    df_disc = df.copy()
    for col in num_cols:
        if df[col].nunique() > 5:
            df_disc[col] = pd.qcut(df[col], 5, duplicates='drop')

    # Iterar por todas las columnas excepto el target
    for col in df_disc.drop(columns=[target_col]).columns:
        tabla = pd.crosstab(df_disc[col], df_disc[target_col])
        chi2, p, dof, expected = chi2_contingency(tabla)
        resultados.append({
            'Variable': col,
            'Chi2': chi2,
            'GL': dof,
            'p-valor': p,
            'Asociación significativa': 'Sí' if p < alpha else 'No'
        })
    resumen = pd.DataFrame(resultados).sort_values(by='p-valor')
    return resumen

# Función para t-test
def tst(df, target_col='target'):
    continuous_cols = df.select_dtypes(include=['float64','int64']).columns.drop(target_col)
    resultados = []
    for col in continuous_cols:
        grupo0 = df[df[target_col]==0][col]
        grupo1 = df[df[target_col]==1][col]
        t_stat, p_val = ttest_ind(grupo0, grupo1)
        resultados.append({
            'Variable': col,
            'Media target=0': grupo0.mean(),
            'Media target=1': grupo1.mean(),
            'DesvStd target=0': grupo0.std(),
            'DesvStd target=1': grupo1.std(),
            'T-stat': t_stat,
            'p-valor': p_val,
            'Asociación significativa': 'Sí' if p_val < 0.05 else 'No'
        })
    resumen = pd.DataFrame(resultados).sort_values(by='p-valor')
    return resumen

# Función para mostrar tablas y gráficas en Streamlit
def mostrar_tests(df, target_col='target'):
    st.subheader("Chi-cuadrado Test (Variables categóricas)")
    chi2_resumen = chi2_test(df, target_col)
    st.dataframe(chi2_resumen)

    st.subheader("T-test (Variables continuas)")
    ttest_resumen = tst(df, target_col)
    st.dataframe(ttest_resumen)
