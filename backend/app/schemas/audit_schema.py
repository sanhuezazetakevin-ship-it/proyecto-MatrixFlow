from datetime import datetime
from typing import Any

from pydantic import (
    BaseModel,
    ConfigDict,
    field_validator,
)


class AuditResponse(BaseModel):
    id: int
    usuario_id: int | None

    accion: str
    entidad: str

    entidad_id: str | None

    detalle: str | None

    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )

    @field_validator(
        "entidad_id",
        mode="before",
    )
    @classmethod
    def convertir_entidad_id(
        cls,
        value: Any,
    ) -> str | None:

        if value is None:
            return None

        return str(value)

    @field_validator(
        "detalle",
        mode="before",
    )
    @classmethod
    def convertir_detalle(
        cls,
        value: Any,
    ) -> str | None:

        if value is None:
            return None

        if isinstance(value, str):
            return value

        return str(value)