from logging.config import fileConfig
from alembic import context
from sqlalchemy import engine_from_config, pool
from app.core.config import settings
from app.database.connection import Base

# Registrar todos los modelos en Base.metadata.
from app.models.persona_model import Persona
from app.models.face_embedding_model import FaceEmbedding
from app.models.recognition_model import RecognitionLog
from app.models.ml_training_model import MLTrainingRecord
from app.models.usuario_model import Usuario
from app.models.audit_model import AuditLog
from app.models.empresa_model import Empresa
from app.models.sucursal_model import Sucursal
from app.models.categoria_model import Categoria
from app.models.producto_model import Producto
from app.models.inventario_model import Inventario
from app.models.movimiento_inventario_model import MovimientoInventario
from app.models.venta_model import Venta
from app.models.detalle_venta_model import DetalleVenta
from app.models.meta_model import Meta
from app.models.vector_model import Vector
from app.models.vector_valor_model import VectorValor
from app.models.matriz_model import Matriz
from app.models.matriz_valor_model import MatrizValor
from app.models.operacion_model import Operacion
from app.models.operacion_entrada_model import OperacionEntrada
from app.models.operacion_resultado_model import OperacionResultado

config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL.replace("%", "%%"))
target_metadata = Base.metadata

def run_migrations_offline():
    context.configure(url=settings.DATABASE_URL, target_metadata=target_metadata, literal_binds=True, compare_type=True)
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    connectable = engine_from_config(config.get_section(config.config_ini_section), prefix="sqlalchemy.", poolclass=pool.NullPool)
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata, compare_type=True)
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
