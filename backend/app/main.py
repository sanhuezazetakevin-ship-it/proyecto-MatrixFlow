from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.database.connection import Base, engine
from app.api.routes.personas import router as personas_router
from app.api.routes.recognition import router as recognition_router
from app.api.routes.ml import router as ml_router
from app.api.routes.models import router as models_router
from app.api.routes.probabilities import router as probabilities_router
from app.api.routes.auth import router as auth_router
from app.api.routes.admin import router as admin_router
from app.api.routes import empresas
from app.api.routes import sucursales
from app.models.sucursal_model import Sucursal
from app.api.routes import categorias
from app.models.categoria_model import Categoria
from app.api.routes import productos
from app.models.producto_model import Producto
from app.models.inventario_model import Inventario
from app.models.movimiento_inventario_model import MovimientoInventario
from app.api.routes import inventario
from app.models.venta_model import Venta
from app.models.detalle_venta_model import DetalleVenta
from app.api.routes import ventas
from app.models.meta_model import Meta
from app.api.routes import metas
from app.models.vector_model import Vector
from app.models.vector_valor_model import VectorValor
from app.api.routes import vectores
from app.models.matriz_model import Matriz
from app.models.matriz_valor_model import MatrizValor
from app.api.routes import matrices
from app.models.operacion_model import Operacion
from app.models.operacion_entrada_model import OperacionEntrada
from app.models.operacion_resultado_model import OperacionResultado
from app.api.routes import operaciones
from app.api.routes import analisis
from app.api.routes import reportes
from app.models.audit_log_model import AuditLog


from app.models import (
    Persona,
    FaceEmbedding,
    RecognitionLog,
    MLTrainingRecord,
)


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
)
app.include_router(personas_router)
app.include_router(recognition_router)
app.include_router(ml_router)
app.include_router(models_router)
app.include_router(probabilities_router)
app.include_router(auth_router)
app.include_router(admin_router)
app.include_router(empresas.router)
app.include_router(sucursales.router)
app.include_router(categorias.router)
app.include_router(productos.router)        
app.include_router(inventario.router)
app.include_router(ventas.router)
app.include_router(metas.router)
app.include_router(vectores.router)
app.include_router(matrices.router)
app.include_router(operaciones.router)
app.include_router(analisis.router)
app.include_router(reportes.router)

origins = [
    origin.strip()
    for origin in settings.CORS_ORIGINS.split(",")
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {
        "message": "Backend del Sistema Inteligente de Reconocimiento Facial",
        "version": settings.APP_VERSION
    }


@app.post("/api/contacto")
def contacto(data: dict):
    return {
        "success": True,
        "mensaje": "Consulta recibida correctamente",
        "contacto": data
    }
