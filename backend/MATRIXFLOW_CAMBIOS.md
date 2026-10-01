# MatrixFlow - paquete consolidado

## Incluido
- RBAC oficial del proyecto: `consulta`, `operador`, `administrador`.
- Auditoría integrada en productos, inventario, ventas, administración y personas.
- Seguridad de personas y biometría: acceso propio/admin, límites de archivo y errores internos no expuestos.
- Reconocimiento facial protegido y compatible con embeddings `buffalo_l` existentes.
- InsightFace con carga diferida y detección 320x320 configurable para reducir arranque/CPU/RAM en Railway.
- Docker/Railway con `$PORT`, un worker, proxy headers y healthcheck.
- CORS por variable de entorno y preparado para dominio HTTPS de Vercel.
- `psycopg` 3 y normalización automática de URLs `postgresql://`/`postgres://`.
- Bloqueo de fila (`SELECT ... FOR UPDATE`) en movimientos de inventario y venta/anulación para reducir carreras de stock.
- Validaciones de imágenes, tamaño, DNI, cantidades y esquemas existentes.
- Alembic configurado para migraciones futuras.
- Tests existentes de RBAC, auditoría, álgebra/biometría más comprobaciones de configuración de producción.

## Importante para HTTPS/cámara
El backend NO debe intentar servir TLS directamente dentro del contenedor. Railway termina HTTPS y reenvía la solicitud al Uvicorn interno. En Vercel, `VITE_API_BASE_URL` debe ser una URL `https://...up.railway.app`. `getUserMedia` del navegador requiere contexto seguro (HTTPS o localhost).

## No incluido en este ZIP
El frontend no venía en el archivo recibido. Por ello no se puede reemplazar aquí su `VITE_API_BASE_URL`; debe apuntarse a la URL HTTPS pública de Railway al desplegar Vercel.
