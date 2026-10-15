from item_a_modelo import *

# Alternativa 1: substituir D1 por um disco duas vezes mais rápido
resultado_d1_rapido = resolver_e_exibir(
    taxa_q=5.85,
    taxa_u=1.5,
    terminais=50,
    d1_factor=2.0
)

# Alternativa 2: substituir a CPU por uma duas vezes mais rápida
resultado_cpu_rapida = resolver_e_exibir(
    taxa_q=5.85,
    taxa_u=1.5,
    terminais=50,
    cpu_factor=2.0
)