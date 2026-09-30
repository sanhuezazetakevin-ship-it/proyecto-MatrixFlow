from decimal import Decimal

import pytest
from pydantic import ValidationError

from app.schemas.inventario_schema import MovimientoCreate
from app.schemas.venta_schema import DetalleVentaCreate, VentaCreate


def test_movimiento_rechaza_cantidad_no_positiva():
    with pytest.raises(ValidationError):
        MovimientoCreate(tipo="SALIDA", cantidad=Decimal("0"))


def test_detalle_venta_rechaza_cantidad_negativa():
    with pytest.raises(ValidationError):
        DetalleVentaCreate(producto_id=1, cantidad=Decimal("-1"))


def test_venta_requiere_productos():
    with pytest.raises(ValidationError):
        VentaCreate(sucursal_id=1, productos=[])
