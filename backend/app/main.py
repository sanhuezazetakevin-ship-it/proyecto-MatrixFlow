import logging

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError
from starlette.exceptions import (
    HTTPException as StarletteHTTPException,
)

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
from app.models.audit_log_model import AuditLog
from app.api.routes import operaciones
from app.api.routes import analisis
from app.api.routes import reportes



from app.models import (
    Persona,
    FaceEmbedding,
    RecognitionLog,
    MLTrainingRecord,
)


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("app")

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


# ==================================================
# MANEJO GLOBAL DE ERRORES
# ==================================================
# Todas las respuestas de error conservan la clave
# "detail" (texto), porque el frontend la lee.

def _headers_cors(request: Request) -> dict:
    origin = request.headers.get("origin")

    if origin and origin in origins:
        return {
            "Access-Control-Allow-Origin": origin,
            "Access-Control-Allow-Credentials": "true",
        }

    return {}


@app.exception_handler(StarletteHTTPException)
async def manejar_http_exception(
    request: Request,
    exc: StarletteHTTPException,
):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "detail": exc.detail,
        },
        headers={**_headers_cors(request), **(getattr(exc, "headers", None) or {})},
    )


@app.exception_handler(RequestValidationError)
async def manejar_validacion(
    request: Request,
    exc: RequestValidationError,
):
    errores = []

    for error in exc.errors():
        campo = ".".join(
            str(parte) for parte in error["loc"][1:]
        )

        mensaje = error["msg"].removeprefix(
            "Value error, "
        )

        errores.append(
            {
                "campo": campo,
                "mensaje": mensaje,
            }
        )

    detalle = "; ".join(
        f"{e['campo']}: {e['mensaje']}"
        if e["campo"]
        else e["mensaje"]
        for e in errores
    )

    return JSONResponse(
        status_code=422,
        content={
            "success": False,
            "detail": detalle or "Datos inválidos.",
            "errores": errores,
        },
    )


@app.exception_handler(IntegrityError)
async def manejar_integridad(
    request: Request,
    exc: IntegrityError,
):
    logger.warning(
        "Conflicto de integridad en %s %s: %s",
        request.method,
        request.url.path,
        exc.orig,
    )

    return JSONResponse(
        status_code=409,
        content={
            "success": False,
            "detail": (
                "La operación entra en conflicto con "
                "datos existentes (por ejemplo, un "
                "valor duplicado)."
            ),
        },
        headers=_headers_cors(request),
    )


@app.exception_handler(Exception)
async def manejar_error_interno(
    request: Request,
    exc: Exception,
):
    logger.exception(
        "Error no controlado en %s %s",
        request.method,
        request.url.path,
    )

    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "detail": "Error interno del servidor.",
        },
        headers=_headers_cors(request),
    )


@app.get("/health")
def health():
    return {"status": "ok", "service": "matrixflow-backend"}


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
