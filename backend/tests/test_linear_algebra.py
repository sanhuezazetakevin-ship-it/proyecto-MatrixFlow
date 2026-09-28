from app.algorithms.linear_algebra import (
    LinearAlgebraError,
    linear_algebra_engine,
)


engine = linear_algebra_engine


def main():

    print("\n=== VECTORES ===")

    ventas = [
        5900,
        7200,
        4800,
        8100,
        6500,
    ]

    metas = [
        7000,
        7000,
        5000,
        8000,
        7000,
    ]

    print(
        "Suma:",
        engine.sum_vector(
            ventas,
            metas,
        ),
    )

    print(
        "Resta:",
        engine.subtract_vector(
            ventas,
            metas,
        ),
    )

    print(
        "Escalar x 2:",
        engine.scalar_multiply_vector(
            ventas,
            2,
        ),
    )

    print(
        "Producto punto:",
        engine.dot_product(
            ventas,
            metas,
        ),
    )

    print("\n=== COMBINACIÓN LINEAL ===")

    print(
        engine.linear_combination(
            [
                ventas,
                metas,
            ],
            [
                0.7,
                0.3,
            ],
        )
    )

    print("\n=== MATRICES ===")

    matriz_a = [
        [5900, 6200, 6800],
        [7200, 7500, 7900],
        [4800, 5100, 5500],
    ]

    matriz_b = [
        [6000, 6500, 7000],
        [7000, 7600, 8000],
        [5000, 5200, 5600],
    ]

    print(
        "Suma:",
        engine.add_matrix(
            matriz_a,
            matriz_b,
        ),
    )

    print(
        "Resta:",
        engine.subtract_matrix(
            matriz_a,
            matriz_b,
        ),
    )

    print(
        "Transpuesta:",
        engine.transpose_matrix(
            matriz_a
        ),
    )

    print(
        "Escalar x 0.5:",
        engine.scalar_multiply_matrix(
            matriz_a,
            0.5,
        ),
    )

    print(
        "Multiplicación:",
        engine.multiply_matrix(
            matriz_a,
            matriz_b,
        ),
    )

    print("\n=== VALIDACIÓN ===")

    try:
        engine.sum_vector(
            [1, 2, 3],
            [1, 2],
        )

    except LinearAlgebraError as error:
        print(
            "Error controlado:",
            error,
        )


if __name__ == "__main__":
    main()