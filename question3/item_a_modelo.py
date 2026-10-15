from line_solver import (
    Network,
    Source,
    Queue,
    Delay,
    Sink,
    OpenClass,
    ClosedClass,
    SchedStrategy,
    Exp,
    MVA
)


def construir_modelo(
    taxa_q=3.0,
    taxa_u=1.5,
    terminais=50,
    cpu_factor=1.0,
    d1_factor=1.0,
):

    model = Network("Exercicio 3 - Capitulo 6")

    source = Source(model, "Source")
    cpu = Queue(model, "CPU", SchedStrategy.PS)
    d1 = Queue(model, "D1", SchedStrategy.PS)
    d2 = Queue(model, "D2", SchedStrategy.PS)
    think = Delay(model, "Think")
    sink = Sink(model, "Sink")

    Q = OpenClass(model, "Consultas")
    U = OpenClass(model, "Atualizacoes")

    I = ClosedClass(model, "Interativos", terminais, think)

    servicos = {
        cpu: {
            Q: 0.060 / cpu_factor,
            U: 0.100 / cpu_factor,
            I: 0.090 / cpu_factor,
        },
        d1: {
            Q: 0.030 / d1_factor,
            U: 0.030 / d1_factor,
            I: 0.045 / d1_factor,
        },
        d2: {
            Q: 0.060,
            U: 0.090,
        },
    }

    for centro, classes in servicos.items():
        for classe, demanda in classes.items():
            centro.set_service(classe, Exp(1.0 / demanda))

    source.set_arrival(Q, Exp(taxa_q))
    source.set_arrival(U, Exp(taxa_u))

    think.set_service(I, Exp(1.0 / 15.0))

    P = model.init_routing_matrix()

    for classe in [Q, U]:
        P.add_route(classe, source, cpu, 1.0)
        P.add_route(classe, cpu, d1, 1.0)
        P.add_route(classe, d1, d2, 1.0)
        P.add_route(classe, d2, sink, 1.0)

    P.add_route(I, think, cpu, 1.0)
    P.add_route(I, cpu, d1, 1.0)
    P.add_route(I, d1, think, 1.0)

    model.link(P)

    return model


def resolver_e_exibir(**parametros):
    modelo = construir_modelo(**parametros)

    solver = MVA(modelo)
    resultados = solver.avg_table()

    print(resultados)

    return resultados


if __name__ == "__main__":
    resultados_base = resolver_e_exibir()