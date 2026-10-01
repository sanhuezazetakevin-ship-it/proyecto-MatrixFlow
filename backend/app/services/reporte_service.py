from decimal import Decimal
from datetime import date

from app.models.meta_model import Meta
from sqlalchemy import (
    func,
    case,
)
from app.models.detalle_venta_model import DetalleVenta
from sqlalchemy.orm import Session

from app.models.empresa_model import Empresa
from app.models.sucursal_model import Sucursal
from app.models.producto_model import Producto
from app.models.venta_model import Venta
from app.models.inventario_model import Inventario


class ReporteService:

    # ==================================================
    # DASHBOARD EMPRESARIAL
    # ==================================================

    def obtener_dashboard(
        self,
        empresa_id: int,
        db: Session,
    ):

        # ----------------------------------------------
        # 1. Validar empresa
        # ----------------------------------------------

        empresa = (
            db.query(Empresa)
            .filter(
                Empresa.id == empresa_id
            )
            .first()
        )

        if not empresa:
            raise ValueError(
                "La empresa no existe."
            )

        # ----------------------------------------------
        # 2. Obtener sucursales activas
        # ----------------------------------------------

        sucursales = (
            db.query(Sucursal)
            .filter(
                Sucursal.empresa_id == empresa_id,
                Sucursal.activo.is_(True),
            )
            .order_by(
                Sucursal.id.asc()
            )
            .all()
        )

        sucursal_ids = [
            sucursal.id
            for sucursal in sucursales
        ]

        # ----------------------------------------------
        # 3. Cantidad de sucursales
        # ----------------------------------------------

        total_sucursales = len(
            sucursales
        )

        # ----------------------------------------------
        # 4. Productos de la empresa
        # ----------------------------------------------

        total_productos = (
            db.query(
                func.count(Producto.id)
            )
            .filter(
                Producto.empresa_id
                == empresa_id,
                Producto.activo.is_(True),
            )
            .scalar()
            or 0
        )

        # ----------------------------------------------
        # Si no existen sucursales activas,
        # devolvemos dashboard vacío
        # ----------------------------------------------

        if not sucursal_ids:

            return {
                "empresa_id": empresa_id,
                "resumen": {
                    "total_sucursales": 0,
                    "total_productos": (
                        total_productos
                    ),
                    "cantidad_ventas": 0,
                    "ventas_completadas": (
                        Decimal("0")
                    ),
                    "stock_total": (
                        Decimal("0")
                    ),
                    "productos_stock_bajo": 0,
                },
                "ventas_por_sucursal": [],
            }

        # ----------------------------------------------
        # 5. Cantidad de ventas COMPLETADAS
        # ----------------------------------------------

        cantidad_ventas = (
            db.query(
                func.count(Venta.id)
            )
            .filter(
                Venta.sucursal_id.in_(
                    sucursal_ids
                ),
                Venta.estado
                == "COMPLETADA",
            )
            .scalar()
            or 0
        )

        # ----------------------------------------------
        # 6. Total vendido
        # ----------------------------------------------

        ventas_completadas = (
            db.query(
                func.coalesce(
                    func.sum(Venta.total),
                    0,
                )
            )
            .filter(
                Venta.sucursal_id.in_(
                    sucursal_ids
                ),
                Venta.estado
                == "COMPLETADA",
            )
            .scalar()
            or Decimal("0")
        )

        # ----------------------------------------------
        # 7. Stock total
        # ----------------------------------------------

        stock_total = (
            db.query(
                func.coalesce(
                    func.sum(
                        Inventario.stock_actual
                    ),
                    0,
                )
            )
            .filter(
                Inventario.sucursal_id.in_(
                    sucursal_ids
                )
            )
            .scalar()
            or Decimal("0")
        )

        # ----------------------------------------------
        # 8. Productos con stock bajo
        #
        # stock_actual <= stock_minimo
        # ----------------------------------------------

        productos_stock_bajo = (
            db.query(
                func.count(
                    Inventario.id
                )
            )
            .filter(
                Inventario.sucursal_id.in_(
                    sucursal_ids
                ),
                Inventario.stock_actual
                <= Inventario.stock_minimo,
            )
            .scalar()
            or 0
        )

        # ----------------------------------------------
        # 9. Ventas agrupadas por sucursal
        # ----------------------------------------------

        ventas_query = (
            db.query(
                Venta.sucursal_id,
                func.coalesce(
                    func.sum(Venta.total),
                    0,
                ).label(
                    "total_ventas"
                ),
            )
            .filter(
                Venta.sucursal_id.in_(
                    sucursal_ids
                ),
                Venta.estado
                == "COMPLETADA",
            )
            .group_by(
                Venta.sucursal_id
            )
            .all()
        )

        ventas_map = {
            sucursal_id: total
            for sucursal_id, total
            in ventas_query
        }

        # ----------------------------------------------
        # 10. Construir información por sucursal
        # ----------------------------------------------

        ventas_por_sucursal = []

        for sucursal in sucursales:

            total = ventas_map.get(
                sucursal.id,
                Decimal("0"),
            )

            ventas_por_sucursal.append(
                {
                    "sucursal_id": (
                        sucursal.id
                    ),
                    "sucursal": (
                        sucursal.nombre
                    ),
                    "total_ventas": total,
                }
            )

        # ----------------------------------------------
        # 11. Respuesta
        # ----------------------------------------------

        return {
            "empresa_id": empresa_id,

            "resumen": {
                "total_sucursales": (
                    total_sucursales
                ),
                "total_productos": (
                    total_productos
                ),
                "cantidad_ventas": (
                    cantidad_ventas
                ),
                "ventas_completadas": (
                    ventas_completadas
                ),
                "stock_total": (
                    stock_total
                ),
                "productos_stock_bajo": (
                    productos_stock_bajo
                ),
            },

            "ventas_por_sucursal": (
                ventas_por_sucursal
            ),
        }

    # ==================================================
    # INDICADORES DE VENTAS VS METAS POR PERÍODO
    # ==================================================

    def obtener_indicadores_periodo(
        self,
        empresa_id: int,
        fecha_inicio: date,
        fecha_fin: date,
        db: Session,
    ):

        # ----------------------------------------------
        # 1. Validar período
        # ----------------------------------------------

        if fecha_fin < fecha_inicio:
            raise ValueError(
                "La fecha final no puede ser menor "
                "que la fecha inicial."
            )

        # ----------------------------------------------
        # 2. Validar empresa
        # ----------------------------------------------

        empresa = (
            db.query(Empresa)
            .filter(
                Empresa.id == empresa_id
            )
            .first()
        )

        if not empresa:
            raise ValueError(
                "La empresa no existe."
            )

        # ----------------------------------------------
        # 3. Sucursales activas
        # ----------------------------------------------

        sucursales = (
            db.query(Sucursal)
            .filter(
                Sucursal.empresa_id == empresa_id,
                Sucursal.activo.is_(True),
            )
            .order_by(
                Sucursal.id.asc()
            )
            .all()
        )

        if not sucursales:
            raise ValueError(
                "La empresa no tiene "
                "sucursales activas."
            )

        sucursal_ids = [
            sucursal.id
            for sucursal in sucursales
        ]

        # ----------------------------------------------
        # 4. Ventas COMPLETADAS del período
        # ----------------------------------------------

        ventas = (
            db.query(
                Venta.sucursal_id,
                func.coalesce(
                    func.sum(Venta.total),
                    0,
                ).label("total"),
            )
            .filter(
                Venta.sucursal_id.in_(
                    sucursal_ids
                ),
                Venta.estado == "COMPLETADA",
                func.date(Venta.created_at)
                >= fecha_inicio,
                func.date(Venta.created_at)
                <= fecha_fin,
            )
            .group_by(
                Venta.sucursal_id
            )
            .all()
        )

        ventas_map = {
            sucursal_id: Decimal(
                str(total)
            )
            for sucursal_id, total
            in ventas
        }

        # ----------------------------------------------
        # 5. Metas EXACTAS del período
        # ----------------------------------------------

        metas = (
            db.query(Meta)
            .filter(
                Meta.sucursal_id.in_(
                    sucursal_ids
                ),
                Meta.tipo == "VENTAS",
                Meta.fecha_inicio
                == fecha_inicio,
                Meta.fecha_fin
                == fecha_fin,
            )
            .all()
        )

        metas_map = {
            meta.sucursal_id: Decimal(
                str(meta.valor_objetivo)
            )
            for meta in metas
        }

        # ----------------------------------------------
        # 6. Validar metas faltantes
        # ----------------------------------------------

        sin_meta = [
            sucursal.nombre
            for sucursal in sucursales
            if sucursal.id
            not in metas_map
        ]

        if sin_meta:
            raise ValueError(
                "Existen sucursales sin una meta "
                "de VENTAS para el período: "
                + ", ".join(sin_meta)
            )

        # ----------------------------------------------
        # 7. Construir indicadores
        # ----------------------------------------------

        detalle = []

        total_ventas = Decimal("0")
        total_metas = Decimal("0")

        for sucursal in sucursales:

            venta = ventas_map.get(
                sucursal.id,
                Decimal("0"),
            )

            meta = metas_map[
                sucursal.id
            ]

            diferencia = (
                venta - meta
            )

            if meta > 0:
                porcentaje = float(
                    venta
                    / meta
                    * Decimal("100")
                )
            else:
                porcentaje = 0.0

            total_ventas += venta
            total_metas += meta

            detalle.append(
                {
                    "sucursal_id": (
                        sucursal.id
                    ),
                    "sucursal": (
                        sucursal.nombre
                    ),
                    "ventas": venta,
                    "meta": meta,
                    "diferencia": diferencia,
                    "porcentaje_cumplimiento": (
                        round(
                            porcentaje,
                            2,
                        )
                    ),
                }
            )

        # ----------------------------------------------
        # 8. Indicadores generales
        # ----------------------------------------------

        diferencia_total = (
            total_ventas
            - total_metas
        )

        if total_metas > 0:

            porcentaje_general = float(
                total_ventas
                / total_metas
                * Decimal("100")
            )

        else:
            porcentaje_general = 0.0

        # ----------------------------------------------
        # 9. Respuesta
        # ----------------------------------------------

        return {
            "empresa_id": empresa_id,
            "fecha_inicio": fecha_inicio,
            "fecha_fin": fecha_fin,

            "total_ventas": total_ventas,
            "total_metas": total_metas,

            "diferencia_total": (
                diferencia_total
            ),

            "porcentaje_cumplimiento": (
                round(
                    porcentaje_general,
                    2,
                )
            ),

            "sucursales": detalle,
        }

    # ==================================================
    # VENTAS POR PRODUCTO Y PERÍODO
    # ==================================================

    def obtener_ventas_productos(
        self,
        empresa_id: int,
        fecha_inicio: date,
        fecha_fin: date,
        db: Session,
    ):
        if fecha_fin < fecha_inicio:
            raise ValueError(
                "La fecha final no puede ser menor "
                "que la fecha inicial."
            )

        empresa = (
            db.query(Empresa)
            .filter(Empresa.id == empresa_id)
            .first()
        )

        if not empresa:
            raise ValueError(
                "La empresa no existe."
            )

        resultados = (
            db.query(
                Producto.id.label("producto_id"),
                Producto.nombre.label("producto"),
                func.coalesce(
                    func.sum(DetalleVenta.cantidad),
                    0,
                ).label("cantidad_vendida"),
                func.coalesce(
                    func.sum(DetalleVenta.subtotal),
                    0,
                ).label("total_vendido"),
            )
            .join(
                DetalleVenta,
                DetalleVenta.producto_id
                == Producto.id,
            )
            .join(
                Venta,
                Venta.id
                == DetalleVenta.venta_id,
            )
            .join(
                Sucursal,
                Sucursal.id
                == Venta.sucursal_id,
            )
            .filter(
                Sucursal.empresa_id == empresa_id,
                Venta.estado == "COMPLETADA",
                func.date(Venta.created_at)
                >= fecha_inicio,
                func.date(Venta.created_at)
                <= fecha_fin,
            )
            .group_by(
                Producto.id,
                Producto.nombre,
            )
            .order_by(
                func.sum(
                    DetalleVenta.subtotal
                ).desc()
            )
            .all()
        )

        productos = [
            {
                "producto_id": item.producto_id,
                "producto": item.producto,
                "cantidad_vendida": (
                    item.cantidad_vendida
                ),
                "total_vendido": (
                    item.total_vendido
                ),
            }
            for item in resultados
        ]

        return {
            "empresa_id": empresa_id,
            "fecha_inicio": fecha_inicio,
            "fecha_fin": fecha_fin,
            "productos": productos,
        }


    # ==================================================
    # ESTADO DEL INVENTARIO
    # ==================================================

    def obtener_estado_inventario(
        self,
        empresa_id: int,
        db: Session,
    ):
        empresa = (
            db.query(Empresa)
            .filter(Empresa.id == empresa_id)
            .first()
        )

        if not empresa:
            raise ValueError(
                "La empresa no existe."
            )

        registros = (
            db.query(
                Inventario,
                Sucursal.nombre.label(
                    "sucursal_nombre"
                ),
                Producto.nombre.label(
                    "producto_nombre"
                ),
            )
            .join(
                Sucursal,
                Sucursal.id
                == Inventario.sucursal_id,
            )
            .join(
                Producto,
                Producto.id
                == Inventario.producto_id,
            )
            .filter(
                Sucursal.empresa_id == empresa_id,
                Sucursal.activo.is_(True),
                Producto.activo.is_(True),
            )
            .order_by(
                Sucursal.id.asc(),
                Producto.nombre.asc(),
            )
            .all()
        )

        productos = []
        stock_bajo = 0
        sin_stock = 0

        for (
            inventario,
            sucursal_nombre,
            producto_nombre,
        ) in registros:

            stock_actual = Decimal(
                str(inventario.stock_actual)
            )

            stock_minimo = Decimal(
                str(inventario.stock_minimo)
            )

            if stock_actual <= 0:
                estado = "SIN_STOCK"
                sin_stock += 1
                stock_bajo += 1

            elif stock_actual <= stock_minimo:
                estado = "STOCK_BAJO"
                stock_bajo += 1

            else:
                estado = "NORMAL"

            productos.append(
                {
                    "inventario_id": (
                        inventario.id
                    ),
                    "sucursal_id": (
                        inventario.sucursal_id
                    ),
                    "sucursal": (
                        sucursal_nombre
                    ),
                    "producto_id": (
                        inventario.producto_id
                    ),
                    "producto": (
                        producto_nombre
                    ),
                    "stock_actual": (
                        stock_actual
                    ),
                    "stock_minimo": (
                        stock_minimo
                    ),
                    "estado": estado,
                }
            )

        return {
            "empresa_id": empresa_id,
            "total_registros": len(productos),
            "stock_bajo": stock_bajo,
            "sin_stock": sin_stock,
            "productos": productos,
        }
reporte_service = ReporteService()