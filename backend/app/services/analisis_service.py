from decimal import Decimal
from datetime import date
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.sucursal_model import Sucursal
from app.models.venta_model import Venta
from app.models.vector_model import Vector
from app.models.vector_valor_model import VectorValor 
from app.models.meta_model import Meta
from app.models.operacion_model import Operacion
from app.models.operacion_entrada_model import (
    OperacionEntrada,
)
from app.models.operacion_resultado_model import (
    OperacionResultado,
)

from app.algorithms.linear_algebra import (
    linear_algebra_engine,
    LinearAlgebraError,
)

class AnalisisService:

    # ==================================================
    # VECTOR DE VENTAS POR SUCURSAL
    # ==================================================

    def generar_vector_ventas(
        self,
        empresa_id: int,
        usuario_id: int,
        db: Session,
    ) -> Vector:

        try:
            # ------------------------------------------
            # 1. Obtener sucursales activas
            # ------------------------------------------

            sucursales = (
                db.query(Sucursal)
                .filter(
                    Sucursal.empresa_id == empresa_id,
                    Sucursal.activo.is_(True),
                )
                .order_by(Sucursal.id.asc())
                .all()
            )

            if not sucursales:
                raise ValueError(
                    "La empresa no tiene sucursales activas."
                )

            # ------------------------------------------
            # 2. Obtener ventas completadas
            #    agrupadas por sucursal
            # ------------------------------------------

            resultados = (
                db.query(
                    Venta.sucursal_id,
                    func.coalesce(
                        func.sum(Venta.total),
                        0,
                    ).label("total_ventas"),
                )
                .filter(
                    Venta.estado == "COMPLETADA",
                    Venta.sucursal_id.in_(
                        [
                            sucursal.id
                            for sucursal in sucursales
                        ]
                    ),
                )
                .group_by(
                    Venta.sucursal_id
                )
                .all()
            )

            # ------------------------------------------
            # 3. Convertir resultados a diccionario
            # ------------------------------------------

            ventas_por_sucursal = {
                sucursal_id: float(total)
                for sucursal_id, total in resultados
            }

            # ------------------------------------------
            # 4. Construir vector
            # ------------------------------------------

            valores = [
                ventas_por_sucursal.get(
                    sucursal.id,
                    0.0,
                )
                for sucursal in sucursales
            ]

            # ------------------------------------------
            # 5. Crear vector
            # ------------------------------------------

            vector = Vector(
                nombre=(
                    f"Ventas empresa {empresa_id} "
                    f"por sucursal"
                ),
                descripcion=(
                    "Vector generado automáticamente "
                    "a partir de ventas completadas. "
                    "Cada posición representa una "
                    "sucursal activa."
                ),
                dimension=len(valores),
                usuario_id=usuario_id,
            )

            db.add(vector)
            db.flush()

            # ------------------------------------------
            # 6. Guardar valores
            # ------------------------------------------

            for posicion, valor in enumerate(
                valores
            ):
                vector_valor = VectorValor(
                    vector_id=vector.id,
                    posicion=posicion,
                    valor=Decimal(str(valor)),
                )

                db.add(vector_valor)

            db.commit()
            db.refresh(vector)

            return vector

        except ValueError:
            db.rollback()
            raise

        except Exception:
            db.rollback()
            raise
    # ==================================================
    # VECTOR DE METAS POR SUCURSAL
    # ==================================================

    def generar_vector_metas(
        self,
        empresa_id: int,
        usuario_id: int,
        db: Session,
    ) -> Vector:

        try:
            # ------------------------------------------
            # 1. Obtener sucursales activas
            # ------------------------------------------

            sucursales = (
                db.query(Sucursal)
                .filter(
                    Sucursal.empresa_id == empresa_id,
                    Sucursal.activo.is_(True),
                )
                .order_by(Sucursal.id.asc())
                .all()
            )

            if not sucursales:
                raise ValueError(
                    "La empresa no tiene sucursales activas."
                )

            sucursal_ids = [
                sucursal.id
                for sucursal in sucursales
            ]

            # ------------------------------------------
            # 2. Obtener metas de ventas
            # ------------------------------------------

            metas = (
                db.query(Meta)
                .filter(
                    Meta.sucursal_id.in_(
                        sucursal_ids
                    ),
                    Meta.tipo == "VENTAS",
                )
                .order_by(
                    Meta.sucursal_id.asc(),
                    Meta.fecha_inicio.desc(),
                )
                .all()
            )

            # ------------------------------------------
            # 3. Tomar la meta más reciente
            #    de cada sucursal
            # ------------------------------------------

            metas_por_sucursal = {}

            for meta in metas:

                if (
                    meta.sucursal_id
                    not in metas_por_sucursal
                ):
                    metas_por_sucursal[
                        meta.sucursal_id
                    ] = float(
                        meta.valor_objetivo
                    )

            # ------------------------------------------
            # 4. Construir vector
            # ------------------------------------------

            valores = [
                metas_por_sucursal.get(
                    sucursal.id,
                    0.0,
                )
                for sucursal in sucursales
            ]

            # ------------------------------------------
            # 5. Crear vector
            # ------------------------------------------

            vector = Vector(
                nombre=(
                    f"Metas empresa {empresa_id} "
                    f"por sucursal"
                ),
                descripcion=(
                    "Vector generado automáticamente "
                    "a partir de las metas de ventas. "
                    "Cada posición representa una "
                    "sucursal activa."
                ),
                dimension=len(valores),
                usuario_id=usuario_id,
            )

            db.add(vector)
            db.flush()

            # ------------------------------------------
            # 6. Guardar valores
            # ------------------------------------------

            for posicion, valor in enumerate(
                valores
            ):
                vector_valor = VectorValor(
                    vector_id=vector.id,
                    posicion=posicion,
                    valor=Decimal(str(valor)),
                )

                db.add(vector_valor)

            db.commit()
            db.refresh(vector)

            return vector

        except ValueError:
            db.rollback()
            raise

        except Exception:
            db.rollback()
            raise
    # ==================================================
    # COMPARAR VENTAS VS METAS
    # ==================================================

    def comparar_ventas_metas(
        self,
        vector_ventas_id: int,
        vector_metas_id: int,
        usuario_id: int,
        db: Session,
    ):
        try:
            # ------------------------------------------
            # 1. Buscar vector de ventas
            # ------------------------------------------

            vector_ventas = (
                db.query(Vector)
                .filter(
                    Vector.id == vector_ventas_id
                )
                .first()
            )

            if not vector_ventas:
                raise ValueError(
                    "El vector de ventas no existe."
                )

            # ------------------------------------------
            # 2. Buscar vector de metas
            # ------------------------------------------

            vector_metas = (
                db.query(Vector)
                .filter(
                    Vector.id == vector_metas_id
                )
                .first()
            )

            if not vector_metas:
                raise ValueError(
                    "El vector de metas no existe."
                )

            # ------------------------------------------
            # 3. Obtener valores ordenados
            # ------------------------------------------

            valores_ventas = [
                float(item.valor)
                for item in sorted(
                    vector_ventas.valores,
                    key=lambda item: item.posicion,
                )
            ]

            valores_metas = [
                float(item.valor)
                for item in sorted(
                    vector_metas.valores,
                    key=lambda item: item.posicion,
                )
            ]

            # ------------------------------------------
            # 4. Validar dimensiones
            # ------------------------------------------

            if (
                vector_ventas.dimension
                != vector_metas.dimension
            ):
                raise ValueError(
                    "Los vectores de ventas y metas "
                    "deben tener la misma dimensión."
                )

            # ------------------------------------------
            # 5. Calcular Ventas - Metas con NumPy
            # ------------------------------------------

            diferencia = (
                linear_algebra_engine.subtract_vector(
                    valores_ventas,
                    valores_metas,
                )
            )

            # ------------------------------------------
            # 6. Calcular cumplimiento general
            # ------------------------------------------

            total_ventas = sum(valores_ventas)
            total_metas = sum(valores_metas)

            if total_metas > 0:
                porcentaje_cumplimiento = (
                    total_ventas
                    / total_metas
                    * 100
                )
            else:
                porcentaje_cumplimiento = 0.0

            # ------------------------------------------
            # 7. Crear operación
            # ------------------------------------------

            operacion = Operacion(
                usuario_id=usuario_id,
                tipo="VENTAS_VS_METAS",
                estado="COMPLETADA",
            )

            db.add(operacion)
            db.flush()

            # ------------------------------------------
            # 8. Guardar vector ventas
            # ------------------------------------------

            entrada_ventas = OperacionEntrada(
                operacion_id=operacion.id,
                tipo_objeto="VECTOR",
                referencia_id=vector_ventas.id,
                nombre=vector_ventas.nombre,
                orden=0,
                datos={
                    "valores": valores_ventas,
                },
            )

            # ------------------------------------------
            # 9. Guardar vector metas
            # ------------------------------------------

            entrada_metas = OperacionEntrada(
                operacion_id=operacion.id,
                tipo_objeto="VECTOR",
                referencia_id=vector_metas.id,
                nombre=vector_metas.nombre,
                orden=1,
                datos={
                    "valores": valores_metas,
                },
            )

            db.add_all([
                entrada_ventas,
                entrada_metas,
            ])

            # ------------------------------------------
            # 10. Guardar resultado
            # ------------------------------------------

            resultado = OperacionResultado(
                operacion_id=operacion.id,
                tipo_resultado="ANALISIS_VENTAS_METAS",
                datos={
                    "ventas": valores_ventas,
                    "metas": valores_metas,
                    "diferencia": diferencia,
                    "total_ventas": total_ventas,
                    "total_metas": total_metas,
                    "porcentaje_cumplimiento": (
                        round(
                            porcentaje_cumplimiento,
                            2,
                        )
                    ),
                },
            )

            db.add(resultado)

            db.commit()
            db.refresh(operacion)

            return operacion

        except (
            ValueError,
            LinearAlgebraError,
        ):
            db.rollback()
            raise

        except Exception:
            db.rollback()
            raise
    # ==================================================
    # ANÁLISIS AUTOMÁTICO DE VENTAS VS METAS
    # POR EMPRESA Y PERÍODO
    # ==================================================

    def analizar_ventas_metas_periodo(
        self,
        empresa_id: int,
        fecha_inicio: date,
        fecha_fin: date,
        usuario_id: int,
        db: Session,
    ):
        try:
            # ------------------------------------------
            # 1. Obtener sucursales activas
            # ------------------------------------------

            sucursales = (
                db.query(Sucursal)
                .filter(
                    Sucursal.empresa_id == empresa_id,
                    Sucursal.activo.is_(True),
                )
                .order_by(Sucursal.id.asc())
                .all()
            )

            if not sucursales:
                raise ValueError(
                    "La empresa no tiene sucursales activas."
                )

            sucursal_ids = [
                sucursal.id
                for sucursal in sucursales
            ]

            # ------------------------------------------
            # 2. Obtener ventas COMPLETADAS del período
            # ------------------------------------------

            ventas_query = (
                db.query(
                    Venta.sucursal_id,
                    func.coalesce(
                        func.sum(Venta.total),
                        0,
                    ).label("total_ventas"),
                )
                .filter(
                    Venta.sucursal_id.in_(sucursal_ids),
                    Venta.estado == "COMPLETADA",
                    func.date(Venta.created_at) >= fecha_inicio,
                    func.date(Venta.created_at) <= fecha_fin,
                )
                .group_by(Venta.sucursal_id)
                .all()
            )

            ventas_por_sucursal = {
                sucursal_id: float(total)
                for sucursal_id, total
                in ventas_query
            }

            # ------------------------------------------
            # 3. Obtener metas EXACTAS del período
            # ------------------------------------------

            metas = (
                db.query(Meta)
                .filter(
                    Meta.sucursal_id.in_(sucursal_ids),
                    Meta.tipo == "VENTAS",
                    Meta.fecha_inicio == fecha_inicio,
                    Meta.fecha_fin == fecha_fin,
                )
                .all()
            )

            metas_por_sucursal = {
                meta.sucursal_id: float(
                    meta.valor_objetivo
                )
                for meta in metas
            }

            # ------------------------------------------
            # 4. Validar metas faltantes
            # ------------------------------------------

            sucursales_sin_meta = [
                sucursal.nombre
                for sucursal in sucursales
                if sucursal.id not in metas_por_sucursal
            ]

            if sucursales_sin_meta:
                raise ValueError(
                    "Existen sucursales sin una meta de "
                    "VENTAS para el período solicitado: "
                    + ", ".join(sucursales_sin_meta)
                )

            # ------------------------------------------
            # 5. Construir vectores con MISMO orden
            # ------------------------------------------

            vector_ventas = [
                ventas_por_sucursal.get(
                    sucursal.id,
                    0.0,
                )
                for sucursal in sucursales
            ]

            vector_metas = [
                metas_por_sucursal[
                    sucursal.id
                ]
                for sucursal in sucursales
            ]

            # ------------------------------------------
            # 6. Álgebra lineal
            # Ventas - Metas
            # ------------------------------------------

            diferencia = (
                linear_algebra_engine.subtract_vector(
                    vector_ventas,
                    vector_metas,
                )
            )

            # ------------------------------------------
            # 7. Totales y cumplimiento
            # ------------------------------------------

            total_ventas = sum(vector_ventas)
            total_metas = sum(vector_metas)

            porcentaje_cumplimiento = (
                (
                    total_ventas
                    / total_metas
                    * 100
                )
                if total_metas > 0
                else 0.0
            )

            # ------------------------------------------
            # 8. Detalle por sucursal
            # ------------------------------------------

            detalle_sucursales = []

            for indice, sucursal in enumerate(
                sucursales
            ):
                venta = vector_ventas[indice]
                meta = vector_metas[indice]

                cumplimiento = (
                    venta / meta * 100
                    if meta > 0
                    else 0.0
                )

                detalle_sucursales.append(
                    {
                        "sucursal_id": sucursal.id,
                        "sucursal": sucursal.nombre,
                        "ventas": venta,
                        "meta": meta,
                        "diferencia": (
                            diferencia[indice]
                        ),
                        "porcentaje_cumplimiento": (
                            round(cumplimiento, 2)
                        ),
                    }
                )

            # ------------------------------------------
            # 9. Guardar operación
            # ------------------------------------------

            operacion = Operacion(
                usuario_id=usuario_id,
                tipo="VENTAS_VS_METAS_PERIODO",
                estado="COMPLETADA",
            )

            db.add(operacion)
            db.flush()

            # ------------------------------------------
            # 10. Guardar vector ventas como snapshot
            # ------------------------------------------

            entrada_ventas = OperacionEntrada(
                operacion_id=operacion.id,
                tipo_objeto="VECTOR_VENTAS",
                referencia_id=None,
                nombre="Ventas por sucursal",
                orden=0,
                datos={
                    "empresa_id": empresa_id,
                    "fecha_inicio": str(fecha_inicio),
                    "fecha_fin": str(fecha_fin),
                    "valores": vector_ventas,
                },
            )

            # ------------------------------------------
            # 11. Guardar vector metas como snapshot
            # ------------------------------------------

            entrada_metas = OperacionEntrada(
                operacion_id=operacion.id,
                tipo_objeto="VECTOR_METAS",
                referencia_id=None,
                nombre="Metas por sucursal",
                orden=1,
                datos={
                    "empresa_id": empresa_id,
                    "fecha_inicio": str(fecha_inicio),
                    "fecha_fin": str(fecha_fin),
                    "valores": vector_metas,
                },
            )

            db.add_all([
                entrada_ventas,
                entrada_metas,
            ])

            # ------------------------------------------
            # 12. Guardar resultado
            # ------------------------------------------

            resultado = OperacionResultado(
                operacion_id=operacion.id,
                tipo_resultado=(
                    "ANALISIS_VENTAS_METAS_PERIODO"
                ),
                datos={
                    "empresa_id": empresa_id,
                    "fecha_inicio": str(fecha_inicio),
                    "fecha_fin": str(fecha_fin),

                    "ventas": vector_ventas,
                    "metas": vector_metas,
                    "diferencia": diferencia,

                    "total_ventas": total_ventas,
                    "total_metas": total_metas,

                    "porcentaje_cumplimiento": round(
                        porcentaje_cumplimiento,
                        2,
                    ),

                    "sucursales": detalle_sucursales,
                },
            )

            db.add(resultado)

            db.commit()
            db.refresh(operacion)

            return operacion

        except (
            ValueError,
            LinearAlgebraError,
        ):
            db.rollback()
            raise

        except Exception:
            db.rollback()
            raise

analisis_service = AnalisisService()