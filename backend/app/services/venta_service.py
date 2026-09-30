from datetime import datetime
from decimal import (
    Decimal,
    ROUND_HALF_UP,
)

from sqlalchemy.orm import Session

from app.services.audit_service import registrar_auditoria
from app.models.detalle_venta_model import DetalleVenta
from app.models.inventario_model import Inventario
from app.models.movimiento_inventario_model import (
    MovimientoInventario,
)
from app.models.producto_model import Producto
from app.models.sucursal_model import Sucursal
from app.models.venta_model import Venta

from app.schemas.venta_schema import VentaCreate


IGV = Decimal("0.18")
DOS_DECIMALES = Decimal("0.01")


class VentaService:

    def _money(
        self,
        value: Decimal,
    ) -> Decimal:
        return value.quantize(
            DOS_DECIMALES,
            rounding=ROUND_HALF_UP,
        )

    def _get_sucursal(
        self,
        sucursal_id: int,
        db: Session,
    ) -> Sucursal:

        sucursal = (
            db.query(Sucursal)
            .filter(
                Sucursal.id == sucursal_id
            )
            .first()
        )

        if not sucursal:
            raise ValueError(
                "La sucursal indicada no existe."
            )

        if not sucursal.activo:
            raise ValueError(
                "La sucursal se encuentra inactiva."
            )

        return sucursal

    def get_by_id(
        self,
        venta_id: int,
        db: Session,
    ) -> Venta:

        venta = (
            db.query(Venta)
            .filter(
                Venta.id == venta_id
            )
            .first()
        )

        if not venta:
            raise ValueError(
                "Venta no encontrada."
            )

        return venta

    def get_all(
        self,
        db: Session,
    ) -> list[Venta]:

        return (
            db.query(Venta)
            .order_by(
                Venta.created_at.desc()
            )
            .all()
        )

    def get_by_sucursal(
        self,
        sucursal_id: int,
        db: Session,
    ) -> list[Venta]:

        self._get_sucursal(
            sucursal_id,
            db,
        )

        return (
            db.query(Venta)
            .filter(
                Venta.sucursal_id
                == sucursal_id
            )
            .order_by(
                Venta.created_at.desc()
            )
            .all()
        )

    def create(
        self,
        data: VentaCreate,
        usuario_id: int,
        db: Session,
    ) -> Venta:

        sucursal = self._get_sucursal(
            data.sucursal_id,
            db,
        )

        # Evitar repetir un producto dentro
        # de la misma venta.
        productos_ids = [
            item.producto_id
            for item in data.productos
        ]

        if len(productos_ids) != len(
            set(productos_ids)
        ):
            raise ValueError(
                "No se puede repetir un producto "
                "dentro de la misma venta."
            )

        preparados = []
        subtotal_venta = Decimal("0")

        # ==========================================
        # VALIDAR TODOS LOS PRODUCTOS PRIMERO
        # ==========================================

        for item in sorted(
            data.productos,
            key=lambda item: item.producto_id,
        ):

            producto = (
                db.query(Producto)
                .filter(
                    Producto.id
                    == item.producto_id
                )
                .first()
            )

            if not producto:
                raise ValueError(
                    f"El producto {item.producto_id} "
                    "no existe."
                )

            if not producto.activo:
                raise ValueError(
                    f"El producto {producto.nombre} "
                    "se encuentra inactivo."
                )

            if (
                producto.empresa_id
                != sucursal.empresa_id
            ):
                raise ValueError(
                    f"El producto {producto.nombre} "
                    "no pertenece a la empresa "
                    "de esta sucursal."
                )

            inventario = (
                db.query(Inventario)
                .filter(
                    Inventario.sucursal_id
                    == data.sucursal_id,
                    Inventario.producto_id
                    == producto.id,
                )
                .with_for_update()
                .first()
            )

            if not inventario:
                raise ValueError(
                    f"No existe inventario para "
                    f"{producto.nombre} en esta sucursal."
                )

            cantidad = item.cantidad

            if inventario.stock_actual < cantidad:
                raise ValueError(
                    f"Stock insuficiente para "
                    f"{producto.nombre}. "
                    f"Disponible: "
                    f"{inventario.stock_actual}."
                )

            precio = self._money(
                producto.precio
            )

            subtotal_item = self._money(
                precio * cantidad
            )

            subtotal_venta += subtotal_item

            preparados.append(
                {
                    "producto": producto,
                    "inventario": inventario,
                    "cantidad": cantidad,
                    "precio": precio,
                    "subtotal": subtotal_item,
                }
            )

        # ==========================================
        # CALCULAR TOTALES
        # ==========================================

        subtotal_venta = self._money(
            subtotal_venta
        )

        impuesto = self._money(
            subtotal_venta * IGV
        )

        total = self._money(
            subtotal_venta + impuesto
        )

        # ==========================================
        # CREAR VENTA
        # ==========================================

        numero_temporal = (
            "TEMP-"
            + datetime.utcnow().strftime(
                "%Y%m%d%H%M%S%f"
            )
        )

        venta = Venta(
            sucursal_id=data.sucursal_id,
            usuario_id=usuario_id,
            numero_venta=numero_temporal,
            subtotal=subtotal_venta,
            impuesto=impuesto,
            total=total,
            estado="COMPLETADA",
        )

        try:
            db.add(venta)

            # Obtener venta.id sin hacer commit.
            db.flush()

            venta.numero_venta = (
                f"V-{venta.id:08d}"
            )

            # ======================================
            # DETALLES + INVENTARIO
            # ======================================

            for item in preparados:

                producto = item["producto"]
                inventario = item["inventario"]
                cantidad = item["cantidad"]

                detalle = DetalleVenta(
                    venta_id=venta.id,
                    producto_id=producto.id,
                    cantidad=cantidad,
                    precio_unitario=item["precio"],
                    subtotal=item["subtotal"],
                )

                db.add(detalle)

                stock_anterior = (
                    inventario.stock_actual
                )

                stock_nuevo = (
                    stock_anterior - cantidad
                )

                inventario.stock_actual = (
                    stock_nuevo
                )

                movimiento = MovimientoInventario(
                    inventario_id=inventario.id,
                    tipo="SALIDA",
                    cantidad=cantidad,
                    stock_anterior=stock_anterior,
                    stock_nuevo=stock_nuevo,
                    motivo=(
                        f"Venta {venta.numero_venta}"
                    ),
                    usuario_id=usuario_id,
                )

                db.add(movimiento)

            # ======================================
            # UN SOLO COMMIT
            # ======================================

            registrar_auditoria(
                db=db,
                usuario_id=usuario_id,
                accion="CREAR",
                entidad="venta",
                entidad_id=venta.id,
                detalle={
                    "numero_venta": venta.numero_venta,
                    "sucursal_id": venta.sucursal_id,
                    "total": str(venta.total),
                    "productos": len(preparados),
                },
            )

            db.commit()
            db.refresh(venta)

        except Exception:
            db.rollback()
            raise

        return venta
    def anular(
        self,
        venta_id: int,
        usuario_id: int,
        db: Session,
    ) -> Venta:

        venta = self.get_by_id(
            venta_id,
            db,
        )
        
        db.refresh(venta, with_for_update=True)

        # ==========================================
        # VALIDAR ESTADO
        # ==========================================

        if venta.estado == "ANULADA":
            raise ValueError(
                "La venta ya se encuentra anulada."
            )

        if venta.estado != "COMPLETADA":
            raise ValueError(
                "Solo se pueden anular ventas completadas."
            )

        try:

            # ======================================
            # DEVOLVER PRODUCTOS AL INVENTARIO
            # ======================================

            for detalle in sorted(
                venta.detalles,
                key=lambda detalle: detalle.producto_id,
            ):

                inventario = (
                    db.query(Inventario)
                    .filter(
                        Inventario.sucursal_id
                        == venta.sucursal_id,
                        Inventario.producto_id
                        == detalle.producto_id,
                    )
                    .with_for_update()
                    .first()
                )

                if not inventario:
                    raise ValueError(
                        f"No existe inventario para "
                        f"el producto "
                        f"{detalle.producto_id}."
                    )

                stock_anterior = (
                    inventario.stock_actual
                )

                stock_nuevo = (
                    stock_anterior
                    + detalle.cantidad
                )

                inventario.stock_actual = (
                    stock_nuevo
                )

                movimiento = MovimientoInventario(
                    inventario_id=inventario.id,
                    tipo="ENTRADA",
                    cantidad=detalle.cantidad,
                    stock_anterior=stock_anterior,
                    stock_nuevo=stock_nuevo,
                    motivo=(
                        f"Anulación de venta "
                        f"{venta.numero_venta}"
                    ),
                    usuario_id=usuario_id,
                )

                db.add(movimiento)

            # ======================================
            # CAMBIAR ESTADO
            # ======================================

            venta.estado = "ANULADA"

            # ======================================
            # UNA SOLA TRANSACCIÓN
            # ======================================

            registrar_auditoria(
                db=db,
                usuario_id=usuario_id,
                accion="ANULAR",
                entidad="venta",
                entidad_id=venta.id,
                detalle={
                    "numero_venta": venta.numero_venta,
                    "total": str(venta.total),
                },
            )

            db.commit()
            db.refresh(venta)

        except ValueError:
            db.rollback()
            raise

        except Exception:
            db.rollback()
            raise

        return venta

    def get_completadas(
        self,
        db: Session,
    ) -> list[Venta]:

        return (
            db.query(Venta)
            .filter(
                Venta.estado == "COMPLETADA"
            )
            .order_by(
                Venta.created_at.desc()
            )
            .all()
        )
venta_service = VentaService()