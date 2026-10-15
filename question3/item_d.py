from item_a_modelo import *
import pandas as pd
import matplotlib.pyplot as plt

linhas = []

for M in range(50, 251, 10):
    resultados = resolver_e_exibir(
        taxa_q=5.85,
        taxa_u=1.5,
        terminais=M,
        cpu_factor=2.0
    )

    print(f"Terminais: {M} \n\n")

    linhas.append({
        "Terminais": M,
        "R_Q": resultados[resultados["JobClass"] == "Consultas"]["RespT"].sum(),
        "R_U": resultados[resultados["JobClass"] == "Atualizacoes"]["RespT"].sum(),
        "R_I": resultados[(resultados["JobClass"] == "Interativos") & (resultados["Station"] != "Think")]["RespT"].sum()
    })

df = pd.DataFrame(linhas)

for coluna in ["R_Q", "R_U", "R_I"]:
    plt.plot(df["Terminais"], df[coluna], label=coluna)

plt.axhline(1.5, linestyle="--", label="Limite: 1,5 s")
plt.xlabel("Número de terminais")
plt.ylabel("Tempo médio de resposta (s)")
plt.title("Tempo de resposta versus número de terminais")
plt.legend()
plt.grid(True)
plt.show()