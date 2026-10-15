import numpy as np
from question1 import *

D_balanceado = np.array([
    [0.105, 0.375],
    [0.090, 0.480],
    [0.090, 0.240]
])

resultado_balanceado = mva_exato(
    (3, 1), D_balanceado
)[(3, 1)]

aprox_balanceado = mva_aproximado(
    (3, 1), D_balanceado, tolerancia=0.001
)

print("=== MVA EXATO: CARGA BALANCEADA ===")
print("Throughput Q e U:", resultado_balanceado["X"])
print("Resposta média Q e U:", resultado_balanceado["R_centro"].sum(axis=0))
print("Clientes médios por centro:", resultado_balanceado["n_centro"])

print("\n=== MVA APROXIMADO: CARGA BALANCEADA ===")
print("Throughput Q e U:", aprox_balanceado["X"])
print("Resposta média Q e U:", aprox_balanceado["R"])
print("Iterações:", aprox_balanceado["iteracoes"])

original = mva_exato((3, 1), D)[(3, 1)]

X_original = original["X"]
R_original = original["R_centro"].sum(axis=0)

X_novo = resultado_balanceado["X"]
R_novo = resultado_balanceado["R_centro"].sum(axis=0)

print("\n=== VARIAÇÃO PERCENTUAL ===")

for r, classe in enumerate(["Q", "U"]):
    delta_X = (X_novo[r] / X_original[r] - 1) * 100
    delta_R = (R_novo[r] / R_original[r] - 1) * 100

    print(
        f"{classe}: throughput = {delta_X:+.2f}%; "
        f"tempo de resposta = {delta_R:+.2f}%"
    )