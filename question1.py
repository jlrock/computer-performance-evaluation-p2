import itertools
import numpy as np

D = np.array([
    [0.105, 0.375],
    [0.180, 0.480],
    [0.000, 0.240]
])


def mva_exato(populacao, demandas):
    K, R = demandas.shape
    N = tuple(populacao)

    filas = {(0,) * R: np.zeros(K)}
    resultados = {}

    for total in range(1, sum(N) + 1):
        for estado in itertools.product(
            *[range(n + 1) for n in N]
        ):
            if sum(estado) != total:
                continue

            tempos = np.zeros((K, R))
            throughput = np.zeros(R)

            for r in range(R):
                if estado[r] == 0:
                    continue

                anterior = list(estado)
                anterior[r] -= 1

                n_observado = filas[tuple(anterior)]

                tempos[:, r] = (
                    demandas[:, r] * (1 + n_observado)
                )

                throughput[r] = (
                    estado[r] / tempos[:, r].sum()
                )

            n_centro = np.zeros(K)

            for r in range(R):
                n_centro += throughput[r] * tempos[:, r]

            filas[estado] = n_centro
            resultados[estado] = {
                "R_centro": tempos,
                "X": throughput,
                "n_centro": n_centro
            }

    return resultados


def mva_aproximado(populacao, demandas, tolerancia=0.001, max_iter=10000):
    N = np.array(populacao, dtype=float)
    K, R = demandas.shape

    n = np.zeros((K, R))

    for r in range(R):
        centros = np.where(demandas[:, r] > 0)[0]
        if len(centros) > 0:
            n[centros, r] = N[r] / len(centros)

    for iteracao in range(1, max_iter + 1):
        n_anterior = n.copy()

        tempos = np.zeros((K, R))
        throughput = np.zeros(R)

        for r in range(R):
            if N[r] == 0:
                continue

            n_observado = np.zeros(K)

            for s in range(R):
                if N[s] == 0:
                    continue

                fator = (
                    N[s] - (1 if s == r else 0)
                ) / N[s]

                n_observado += n[:, s] * fator

            tempos[:, r] = (
                demandas[:, r] * (1 + n_observado)
            )

            throughput[r] = N[r] / tempos[:, r].sum()

        n = np.zeros((K, R))

        for r in range(R):
            n[:, r] = throughput[r] * tempos[:, r]

        erro = np.max(np.abs(n - n_anterior))

        if erro < tolerancia:
            break
    else:
        raise RuntimeError("O MVA aproximado não convergiu.")

    return {
        "iteracoes": iteracao,
        "X": throughput,
        "R": tempos.sum(axis=0),
        "n_classes": n.sum(axis=0),
        "n_centros": n.sum(axis=1),
        "R_centro": tempos,
        "erro_final": erro
    }


def mostrar_exato(populacao, demandas):
    resultados = mva_exato(populacao, demandas)
    resultado = resultados[tuple(populacao)]

    print("População:", populacao)
    print("Throughput Q e U:", resultado["X"])
    print("Resposta Q e U:", resultado["R_centro"].sum(axis=0))
    print("Clientes médios por centro:", resultado["n_centro"])

    return resultado


def mostrar_aproximado(populacao, demandas):
    resultado = mva_aproximado(populacao, demandas)

    print("População:", populacao)
    print("Iterações:", resultado["iteracoes"])
    print("Throughput Q e U:", resultado["X"])
    print("Resposta Q e U:", resultado["R"])
    print("Clientes médios por classe:", resultado["n_classes"])
    print("Clientes médios por centro:", resultado["n_centros"])
    print("Erro final:", resultado["erro_final"])

    return resultado


print("=== MODELO ORIGINAL: MVA APROXIMADO ===")
aprox_original = mostrar_aproximado((3, 1), D)

print("\n=== MODELO ORIGINAL: MVA EXATO ===")
exato_original = mostrar_exato((3, 1), D)

print("\n=== ATUALIZAÇÕES TRIPLICADAS: MVA EXATO ===")
exato_triplicado = mostrar_exato((3, 3), D)

print("\n=== ATUALIZAÇÕES TRIPLICADAS: MVA APROXIMADO ===")
aprox_triplicado = mostrar_aproximado((3, 3), D)