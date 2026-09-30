from sqlalchemy.orm import Session

from app.services.audit_service import registrar_auditoria
from app.algorithms.linear_algebra import (
    LinearAlgebraError,
    linear_algebra_engine,
)

from app.models.matriz_model import Matriz
from app.models.operacion_model import Operacion
from app.models.operacion_entrada_model import OperacionEntrada
from app.models.operacion_resultado_model import OperacionResultado
from app.models.vector_model import Vector


class OperacionService:

    # ==================================================
    # UTILIDADES - VECTOR
    # ==================================================

    def _get_vector(
        self,
        vector_id: int,
        db: Session,
    ) -> Vector:

        vector = (
            db.query(Vector)
            .filter(Vector.id == vector_id)
            .first()
        )

        if not vector:
            raise ValueError(
                f"Vector {vector_id} no encontrado."
            )

        return vector

    def _vector_values(
        self,
        vector: Vector,
    ) -> list[float]:

        valores_ordenados = sorted(
            vector.valores,
            key=lambda item: item.posicion,
        )

        return [
            float(valor.valor)
            for valor in valores_ordenados
        ]

    # ==================================================
    # UTILIDADES - MATRIZ
    # ==================================================

    def _get_matriz(
        self,
        matriz_id: int,
        db: Session,
    ) -> Matriz:

        matriz = (
            db.query(Matriz)
            .filter(Matriz.id == matriz_id)
            .first()
        )

        if not matriz:
            raise ValueError(
                f"Matriz {matriz_id} no encontrada."
            )

        return matriz

    def _matriz_values(
        self,
        matriz: Matriz,
    ) -> list[list[float]]:

        resultado = [
            [
                0.0
                for _ in range(matriz.columnas)
            ]
            for _ in range(matriz.filas)
        ]

        for item in matriz.valores:
            resultado[item.fila][item.columna] = float(
                item.valor
            )

        return resultado

    # ==================================================
    # UTILIDADES - OPERACIÓN
    # ==================================================

    def _create_operation(
        self,
        tipo: str,
        usuario_id: int,
        db: Session,
    ) -> Operacion:

        operacion = Operacion(
            tipo=tipo,
            usuario_id=usuario_id,
            estado="COMPLETADA",
        )

        db.add(operacion)
        db.flush()

        registrar_auditoria(
            db=db,
            usuario_id=usuario_id,
            accion="EJECUTAR",
            entidad="operacion",
            entidad_id=operacion.id,
            detalle={"tipo": tipo},
        )

        return operacion

    def _add_vector_input(
        self,
        operacion_id: int,
        vector: Vector,
        orden: int,
        db: Session,
    ) -> list[float]:

        valores = self._vector_values(vector)

        entrada = OperacionEntrada(
            operacion_id=operacion_id,
            tipo_objeto="VECTOR",
            referencia_id=vector.id,
            nombre=vector.nombre,
            orden=orden,
            datos=valores,
        )

        db.add(entrada)

        return valores

    def _add_matrix_input(
        self,
        operacion_id: int,
        matriz: Matriz,
        orden: int,
        db: Session,
    ) -> list[list[float]]:

        valores = self._matriz_values(matriz)

        entrada = OperacionEntrada(
            operacion_id=operacion_id,
            tipo_objeto="MATRIZ",
            referencia_id=matriz.id,
            nombre=matriz.nombre,
            orden=orden,
            datos=valores,
        )

        db.add(entrada)

        return valores

    def _add_scalar_input(
        self,
        operacion_id: int,
        escalar: float,
        orden: int,
        db: Session,
    ) -> None:

        entrada = OperacionEntrada(
            operacion_id=operacion_id,
            tipo_objeto="ESCALAR",
            referencia_id=None,
            nombre="Escalar",
            orden=orden,
            datos=float(escalar),
        )

        db.add(entrada)

    def _save_result(
        self,
        operacion_id: int,
        tipo_resultado: str,
        resultado,
        db: Session,
    ) -> None:

        registro = OperacionResultado(
            operacion_id=operacion_id,
            tipo_resultado=tipo_resultado,
            datos=resultado,
        )

        db.add(registro)

    # ==================================================
    # SUMA VECTOR
    # ==================================================

    def sumar_vectores(
        self,
        vector_a_id: int,
        vector_b_id: int,
        usuario_id: int,
        db: Session,
    ) -> Operacion:

        try:
            vector_a = self._get_vector(
                vector_a_id,
                db,
            )

            vector_b = self._get_vector(
                vector_b_id,
                db,
            )

            valores_a = self._vector_values(
                vector_a
            )

            valores_b = self._vector_values(
                vector_b
            )

            resultado = (
                linear_algebra_engine.sum_vector(
                    valores_a,
                    valores_b,
                )
            )

            operacion = self._create_operation(
                tipo="SUMA_VECTOR",
                usuario_id=usuario_id,
                db=db,
            )

            self._add_vector_input(
                operacion.id,
                vector_a,
                0,
                db,
            )

            self._add_vector_input(
                operacion.id,
                vector_b,
                1,
                db,
            )

            self._save_result(
                operacion.id,
                "VECTOR",
                resultado,
                db,
            )

            db.commit()
            db.refresh(operacion)

            return operacion

        except (ValueError, LinearAlgebraError):
            db.rollback()
            raise

        except Exception:
            db.rollback()
            raise

    # ==================================================
    # RESTA VECTOR
    # ==================================================

    def restar_vectores(
        self,
        vector_a_id: int,
        vector_b_id: int,
        usuario_id: int,
        db: Session,
    ) -> Operacion:

        try:
            vector_a = self._get_vector(
                vector_a_id,
                db,
            )

            vector_b = self._get_vector(
                vector_b_id,
                db,
            )

            valores_a = self._vector_values(
                vector_a
            )

            valores_b = self._vector_values(
                vector_b
            )

            resultado = (
                linear_algebra_engine.subtract_vector(
                    valores_a,
                    valores_b,
                )
            )

            operacion = self._create_operation(
                tipo="RESTA_VECTOR",
                usuario_id=usuario_id,
                db=db,
            )

            self._add_vector_input(
                operacion.id,
                vector_a,
                0,
                db,
            )

            self._add_vector_input(
                operacion.id,
                vector_b,
                1,
                db,
            )

            self._save_result(
                operacion.id,
                "VECTOR",
                resultado,
                db,
            )

            db.commit()
            db.refresh(operacion)

            return operacion

        except (ValueError, LinearAlgebraError):
            db.rollback()
            raise

        except Exception:
            db.rollback()
            raise

    # ==================================================
    # ESCALAR VECTOR
    # ==================================================

    def escalar_vector(
        self,
        vector_id: int,
        escalar: float,
        usuario_id: int,
        db: Session,
    ) -> Operacion:

        try:
            vector = self._get_vector(
                vector_id,
                db,
            )

            valores = self._vector_values(
                vector
            )

            resultado = (
                linear_algebra_engine
                .scalar_multiply_vector(
                    valores,
                    escalar,
                )
            )

            operacion = self._create_operation(
                tipo="ESCALAR_VECTOR",
                usuario_id=usuario_id,
                db=db,
            )

            self._add_vector_input(
                operacion.id,
                vector,
                0,
                db,
            )

            self._add_scalar_input(
                operacion.id,
                escalar,
                1,
                db,
            )

            self._save_result(
                operacion.id,
                "VECTOR",
                resultado,
                db,
            )

            db.commit()
            db.refresh(operacion)

            return operacion

        except (ValueError, LinearAlgebraError):
            db.rollback()
            raise

        except Exception:
            db.rollback()
            raise

    # ==================================================
    # PRODUCTO PUNTO
    # ==================================================

    def producto_punto(
        self,
        vector_a_id: int,
        vector_b_id: int,
        usuario_id: int,
        db: Session,
    ) -> Operacion:

        try:
            vector_a = self._get_vector(
                vector_a_id,
                db,
            )

            vector_b = self._get_vector(
                vector_b_id,
                db,
            )

            valores_a = self._vector_values(
                vector_a
            )

            valores_b = self._vector_values(
                vector_b
            )

            resultado = (
                linear_algebra_engine.dot_product(
                    valores_a,
                    valores_b,
                )
            )

            operacion = self._create_operation(
                tipo="PRODUCTO_PUNTO",
                usuario_id=usuario_id,
                db=db,
            )

            self._add_vector_input(
                operacion.id,
                vector_a,
                0,
                db,
            )

            self._add_vector_input(
                operacion.id,
                vector_b,
                1,
                db,
            )

            self._save_result(
                operacion.id,
                "ESCALAR",
                resultado,
                db,
            )

            db.commit()
            db.refresh(operacion)

            return operacion

        except (ValueError, LinearAlgebraError):
            db.rollback()
            raise

        except Exception:
            db.rollback()
            raise

    # ==================================================
    # SUMA MATRICES
    # ==================================================

    def sumar_matrices(
        self,
        matriz_a_id: int,
        matriz_b_id: int,
        usuario_id: int,
        db: Session,
    ) -> Operacion:

        try:
            matriz_a = self._get_matriz(
                matriz_a_id,
                db,
            )

            matriz_b = self._get_matriz(
                matriz_b_id,
                db,
            )

            valores_a = self._matriz_values(
                matriz_a
            )

            valores_b = self._matriz_values(
                matriz_b
            )

            resultado = (
                linear_algebra_engine.add_matrix(
                    valores_a,
                    valores_b,
                )
            )

            operacion = self._create_operation(
                tipo="SUMA_MATRIZ",
                usuario_id=usuario_id,
                db=db,
            )

            self._add_matrix_input(
                operacion.id,
                matriz_a,
                0,
                db,
            )

            self._add_matrix_input(
                operacion.id,
                matriz_b,
                1,
                db,
            )

            self._save_result(
                operacion.id,
                "MATRIZ",
                resultado,
                db,
            )

            db.commit()
            db.refresh(operacion)

            return operacion

        except (ValueError, LinearAlgebraError):
            db.rollback()
            raise

        except Exception:
            db.rollback()
            raise

    # ==================================================
    # RESTA MATRICES
    # ==================================================

    def restar_matrices(
        self,
        matriz_a_id: int,
        matriz_b_id: int,
        usuario_id: int,
        db: Session,
    ) -> Operacion:

        try:
            matriz_a = self._get_matriz(
                matriz_a_id,
                db,
            )

            matriz_b = self._get_matriz(
                matriz_b_id,
                db,
            )

            valores_a = self._matriz_values(
                matriz_a
            )

            valores_b = self._matriz_values(
                matriz_b
            )

            resultado = (
                linear_algebra_engine.subtract_matrix(
                    valores_a,
                    valores_b,
                )
            )

            operacion = self._create_operation(
                tipo="RESTA_MATRIZ",
                usuario_id=usuario_id,
                db=db,
            )

            self._add_matrix_input(
                operacion.id,
                matriz_a,
                0,
                db,
            )

            self._add_matrix_input(
                operacion.id,
                matriz_b,
                1,
                db,
            )

            self._save_result(
                operacion.id,
                "MATRIZ",
                resultado,
                db,
            )

            db.commit()
            db.refresh(operacion)

            return operacion

        except (ValueError, LinearAlgebraError):
            db.rollback()
            raise

        except Exception:
            db.rollback()
            raise

    # ==================================================
    # MULTIPLICACIÓN MATRICES
    # ==================================================

    def multiplicar_matrices(
        self,
        matriz_a_id: int,
        matriz_b_id: int,
        usuario_id: int,
        db: Session,
    ) -> Operacion:

        try:
            matriz_a = self._get_matriz(
                matriz_a_id,
                db,
            )

            matriz_b = self._get_matriz(
                matriz_b_id,
                db,
            )

            valores_a = self._matriz_values(
                matriz_a
            )

            valores_b = self._matriz_values(
                matriz_b
            )

            resultado = (
                linear_algebra_engine.multiply_matrix(
                    valores_a,
                    valores_b,
                )
            )

            operacion = self._create_operation(
                tipo="MULTIPLICACION_MATRIZ",
                usuario_id=usuario_id,
                db=db,
            )

            self._add_matrix_input(
                operacion.id,
                matriz_a,
                0,
                db,
            )

            self._add_matrix_input(
                operacion.id,
                matriz_b,
                1,
                db,
            )

            self._save_result(
                operacion.id,
                "MATRIZ",
                resultado,
                db,
            )

            db.commit()
            db.refresh(operacion)

            return operacion

        except (ValueError, LinearAlgebraError):
            db.rollback()
            raise

        except Exception:
            db.rollback()
            raise

    # ==================================================
    # TRANSPUESTA MATRIZ
    # ==================================================

    def transponer_matriz(
        self,
        matriz_id: int,
        usuario_id: int,
        db: Session,
    ) -> Operacion:

        try:
            matriz = self._get_matriz(
                matriz_id,
                db,
            )

            valores = self._matriz_values(
                matriz
            )

            resultado = (
                linear_algebra_engine.transpose_matrix(
                    valores
                )
            )

            operacion = self._create_operation(
                tipo="TRANSPUESTA_MATRIZ",
                usuario_id=usuario_id,
                db=db,
            )

            self._add_matrix_input(
                operacion.id,
                matriz,
                0,
                db,
            )

            self._save_result(
                operacion.id,
                "MATRIZ",
                resultado,
                db,
            )

            db.commit()
            db.refresh(operacion)

            return operacion

        except (ValueError, LinearAlgebraError):
            db.rollback()
            raise

        except Exception:
            db.rollback()
            raise

    # ==================================================
    # ESCALAR MATRIZ
    # ==================================================

    def escalar_matriz(
        self,
        matriz_id: int,
        escalar: float,
        usuario_id: int,
        db: Session,
    ) -> Operacion:

        try:
            matriz = self._get_matriz(
                matriz_id,
                db,
            )

            valores = self._matriz_values(
                matriz
            )

            resultado = (
                linear_algebra_engine
                .scalar_multiply_matrix(
                    valores,
                    escalar,
                )
            )

            operacion = self._create_operation(
                tipo="ESCALAR_MATRIZ",
                usuario_id=usuario_id,
                db=db,
            )

            self._add_matrix_input(
                operacion.id,
                matriz,
                0,
                db,
            )

            self._add_scalar_input(
                operacion.id,
                escalar,
                1,
                db,
            )

            self._save_result(
                operacion.id,
                "MATRIZ",
                resultado,
                db,
            )

            db.commit()
            db.refresh(operacion)

            return operacion

        except (ValueError, LinearAlgebraError):
            db.rollback()
            raise

        except Exception:
            db.rollback()
            raise
 # ==================================================
    # COMBINACIÓN LINEAL
    # ==================================================

    def combinacion_lineal(
        self,
        vector_ids: list[int],
        coeficientes: list[float],
        usuario_id: int,
        db: Session,
    ) -> Operacion:

        try:
            if not vector_ids:
                raise ValueError(
                    "Debe proporcionar al menos un vector."
                )

            if len(vector_ids) != len(coeficientes):
                raise ValueError(
                    "La cantidad de vectores debe coincidir "
                    "con la cantidad de coeficientes."
                )

            vectores = [
                self._get_vector(
                    vector_id,
                    db,
                )
                for vector_id in vector_ids
            ]

            valores_vectores = [
                self._vector_values(vector)
                for vector in vectores
            ]

            resultado = (
                linear_algebra_engine.linear_combination(
                    valores_vectores,
                    coeficientes,
                )
            )

            operacion = self._create_operation(
                tipo="COMBINACION_LINEAL",
                usuario_id=usuario_id,
                db=db,
            )

            orden = 0

            for vector, coeficiente in zip(
                vectores,
                coeficientes,
            ):
                self._add_vector_input(
                    operacion.id,
                    vector,
                    orden,
                    db,
                )

                orden += 1

                entrada_coeficiente = OperacionEntrada(
                    operacion_id=operacion.id,
                    tipo_objeto="COEFICIENTE",
                    referencia_id=None,
                    nombre=f"Coeficiente de {vector.nombre}",
                    orden=orden,
                    datos=float(coeficiente),
                )

                db.add(entrada_coeficiente)

                orden += 1

            self._save_result(
                operacion.id,
                "VECTOR",
                resultado,
                db,
            )

            db.commit()
            db.refresh(operacion)

            return operacion

        except (ValueError, LinearAlgebraError):
            db.rollback()
            raise

        except Exception:
            db.rollback()
            raise

    # ==================================================
    # CONSULTAS / HISTORIAL
    # ==================================================

    def get_all(
        self,
        db: Session,
    ) -> list[Operacion]:

        return (
            db.query(Operacion)
            .order_by(
                Operacion.created_at.desc()
            )
            .all()
        )

    def get_by_id(
        self,
        operacion_id: int,
        db: Session,
    ) -> Operacion:

        operacion = (
            db.query(Operacion)
            .filter(
                Operacion.id == operacion_id
            )
            .first()
        )

        if not operacion:
            raise ValueError(
                "Operación no encontrada."
            )

        return operacion


operacion_service = OperacionService()