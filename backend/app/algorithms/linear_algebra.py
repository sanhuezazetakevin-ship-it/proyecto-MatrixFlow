import numpy as np


class LinearAlgebraError(ValueError):
    """Error controlado del motor de álgebra lineal."""
    pass


class LinearAlgebraEngine:

    # ==================================================
    # CONVERSIÓN Y VALIDACIÓN
    # ==================================================

    def validate_vector(
        self,
        values,
    ) -> np.ndarray:

        try:
            vector = np.asarray(
                values,
                dtype=np.float64,
            )
        except (TypeError, ValueError):
            raise LinearAlgebraError(
                "El vector contiene valores inválidos."
            )

        if vector.ndim != 1:
            raise LinearAlgebraError(
                "Los datos deben representar un vector."
            )

        if vector.size == 0:
            raise LinearAlgebraError(
                "El vector no puede estar vacío."
            )

        if not np.all(np.isfinite(vector)):
            raise LinearAlgebraError(
                "El vector contiene valores no finitos."
            )

        return vector

    def validate_matrix(
        self,
        values,
    ) -> np.ndarray:

        try:
            matrix = np.asarray(
                values,
                dtype=np.float64,
            )
        except (TypeError, ValueError):
            raise LinearAlgebraError(
                "La matriz contiene valores inválidos."
            )

        if matrix.ndim != 2:
            raise LinearAlgebraError(
                "Los datos deben representar una matriz."
            )

        if matrix.size == 0:
            raise LinearAlgebraError(
                "La matriz no puede estar vacía."
            )

        if (
            matrix.shape[0] == 0
            or matrix.shape[1] == 0
        ):
            raise LinearAlgebraError(
                "La matriz debe tener filas y columnas."
            )

        if not np.all(np.isfinite(matrix)):
            raise LinearAlgebraError(
                "La matriz contiene valores no finitos."
            )

        return matrix

    # ==================================================
    # VECTORES
    # ==================================================

    def sum_vector(
        self,
        vector_a,
        vector_b,
    ) -> list[float]:

        a = self.validate_vector(vector_a)
        b = self.validate_vector(vector_b)

        if a.shape != b.shape:
            raise LinearAlgebraError(
                "Los vectores deben tener "
                "la misma dimensión."
            )

        return (a + b).tolist()

    def subtract_vector(
        self,
        vector_a,
        vector_b,
    ) -> list[float]:

        a = self.validate_vector(vector_a)
        b = self.validate_vector(vector_b)

        if a.shape != b.shape:
            raise LinearAlgebraError(
                "Los vectores deben tener "
                "la misma dimensión."
            )

        return (a - b).tolist()

    def scalar_multiply_vector(
        self,
        vector,
        scalar: float,
    ) -> list[float]:

        v = self.validate_vector(vector)

        try:
            scalar_value = float(scalar)
        except (TypeError, ValueError):
            raise LinearAlgebraError(
                "El escalar debe ser numérico."
            )

        if not np.isfinite(scalar_value):
            raise LinearAlgebraError(
                "El escalar debe ser un número finito."
            )

        return (
            v * scalar_value
        ).tolist()

    def dot_product(
        self,
        vector_a,
        vector_b,
    ) -> float:

        a = self.validate_vector(vector_a)
        b = self.validate_vector(vector_b)

        if a.shape != b.shape:
            raise LinearAlgebraError(
                "Los vectores deben tener "
                "la misma dimensión para "
                "calcular el producto punto."
            )

        return float(
            np.dot(a, b)
        )

    # ==================================================
    # MATRICES
    # ==================================================

    def add_matrix(
        self,
        matrix_a,
        matrix_b,
    ) -> list[list[float]]:

        a = self.validate_matrix(matrix_a)
        b = self.validate_matrix(matrix_b)

        if a.shape != b.shape:
            raise LinearAlgebraError(
                "Las matrices deben tener "
                "las mismas dimensiones."
            )

        return (a + b).tolist()

    def subtract_matrix(
        self,
        matrix_a,
        matrix_b,
    ) -> list[list[float]]:

        a = self.validate_matrix(matrix_a)
        b = self.validate_matrix(matrix_b)

        if a.shape != b.shape:
            raise LinearAlgebraError(
                "Las matrices deben tener "
                "las mismas dimensiones."
            )

        return (a - b).tolist()

    def multiply_matrix(
        self,
        matrix_a,
        matrix_b,
    ) -> list[list[float]]:

        a = self.validate_matrix(matrix_a)
        b = self.validate_matrix(matrix_b)

        if a.shape[1] != b.shape[0]:
            raise LinearAlgebraError(
                "No se pueden multiplicar las matrices: "
                "las columnas de la primera deben ser "
                "iguales a las filas de la segunda."
            )

        return np.matmul(
            a,
            b,
        ).tolist()

    def transpose_matrix(
        self,
        matrix,
    ) -> list[list[float]]:

        m = self.validate_matrix(matrix)

        return m.T.tolist()

    def scalar_multiply_matrix(
        self,
        matrix,
        scalar: float,
    ) -> list[list[float]]:

        m = self.validate_matrix(matrix)

        try:
            scalar_value = float(scalar)
        except (TypeError, ValueError):
            raise LinearAlgebraError(
                "El escalar debe ser numérico."
            )

        if not np.isfinite(scalar_value):
            raise LinearAlgebraError(
                "El escalar debe ser un número finito."
            )

        return (
            m * scalar_value
        ).tolist()

    # ==================================================
    # COMBINACIONES LINEALES
    # ==================================================

    def linear_combination(
        self,
        vectors,
        coefficients,
    ) -> list[float]:

        if not vectors:
            raise LinearAlgebraError(
                "Debe proporcionar al menos un vector."
            )

        if len(vectors) != len(coefficients):
            raise LinearAlgebraError(
                "Debe existir un coeficiente "
                "por cada vector."
            )

        validated_vectors = [
            self.validate_vector(vector)
            for vector in vectors
        ]

        dimension = validated_vectors[0].shape

        for vector in validated_vectors:

            if vector.shape != dimension:
                raise LinearAlgebraError(
                    "Todos los vectores deben tener "
                    "la misma dimensión."
                )

        try:
            coefficients_array = np.asarray(
                coefficients,
                dtype=np.float64,
            )
        except (TypeError, ValueError):
            raise LinearAlgebraError(
                "Los coeficientes deben ser numéricos."
            )

        if not np.all(
            np.isfinite(coefficients_array)
        ):
            raise LinearAlgebraError(
                "Los coeficientes deben ser finitos."
            )

        result = np.zeros_like(
            validated_vectors[0],
            dtype=np.float64,
        )

        for coefficient, vector in zip(
            coefficients_array,
            validated_vectors,
        ):
            result += coefficient * vector

        return result.tolist()


linear_algebra_engine = LinearAlgebraEngine()