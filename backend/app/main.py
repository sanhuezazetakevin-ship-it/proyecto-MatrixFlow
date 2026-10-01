from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from app.core.config import settings
from app.database.connection import Base, engine
from app.api.routes.personas import router as personas_router
from app.api.routes.recognition import router as recognition_router
from app.api.routes.ml import router as ml_router
from app.api.routes.models import router as models_router
from app.api.routes.probabilities import router as probabilities_router
from app.api.routes.auth import router as auth_router
from app.api.routes.admin import router as admin_router
from app.api.routes import (
    empresas, sucursales, categorias, productos, inventario, ventas, metas,
    vectores, matrices, operaciones, analisis, reportes, auditoria,
)

# Importa los modelos antes de create_all. Alembic es el mecanismo recomendado
# para cambios de esquema; create_all conserva compatibilidad con el proyecto actual.
from app.models import *  # noqa: F401,F403
from app.models.empresa_model import Empresa  # noqa: F401
from app.models.sucursal_model import Sucursal  # noqa: F401
from app.models.categoria_model import Categoria  # noqa: F401
from app.models.producto_model import Producto  # noqa: F401
from app.models.inventario_model import Inventario  # noqa: F401
from app.models.movimiento_inventario_model import MovimientoInventario  # noqa: F401
from app.models.venta_model import Venta  # noqa: F401
from app.models.detalle_venta_model import DetalleVenta  # noqa: F401
from app.models.meta_model import Meta  # noqa: F401
from app.models.vector_model import Vector  # noqa: F401
from app.models.vector_valor_model import VectorValor  # noqa: F401
from app.models.matriz_model import Matriz  # noqa: F401
from app.models.matriz_valor_model import MatrizValor  # noqa: F401
from app.models.operacion_model import Operacion  # noqa: F401
from app.models.operacion_entrada_model import OperacionEntrada  # noqa: F401
from app.models.operacion_resultado_model import OperacionResultado  # noqa: F401

Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.APP_NAME, version=settings.APP_VERSION)

for router in (
    personas_router, recognition_router, ml_router, models_router,
    probabilities_router, auth_router, admin_router, empresas.router,
    sucursales.router, categorias.router, productos.router, inventario.router,
    ventas.router, metas.router, vectores.router, matrices.router,
    operaciones.router, analisis.router, reportes.router, auditoria.router,
):
    app.include_router(router)

origins = [o.strip().rstrip("/") for o in settings.CORS_ORIGINS.split(",") if o.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type", "Accept"],
)


@app.get("/")
def root():
    return {"message": "MatrixFlow Enterprise API", "version": settings.APP_VERSION}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/health/db")
def health_db():
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))
    return {"status": "ok", "database": "connected"}


@app.post("/api/contacto")
def contacto(data: dict):
    # Endpoint público de contacto conservado por compatibilidad con el frontend.
    return {
        "success": True,
        "mensaje": "Consulta recibida correctamente",
        "contacto": data,
    }
