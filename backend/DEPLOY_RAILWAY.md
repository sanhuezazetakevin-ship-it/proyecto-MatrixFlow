# MatrixFlow - Railway + Vercel

## Railway
1. Root Directory: `backend` si el repositorio contiene frontend/backend; si este ZIP es el root, use `.`.
2. Builder: Dockerfile. Railway publica HTTPS aunque Uvicorn escuche HTTP dentro del contenedor.
3. Variables: copie `.env.example` y configure valores reales. Nunca suba `.env`.
4. `CORS_ORIGINS` debe contener el origen HTTPS exacto de Vercel, sin ruta.
5. Healthcheck: `/health`.

## Cámara / HTTPS
El navegador requiere contexto seguro para `getUserMedia`: el frontend debe abrirse por HTTPS y debe llamar a la URL pública `https://...up.railway.app`. No use `http://` desde Vercel. El TLS termina en Railway; FastAPI puede escuchar HTTP internamente.

## Facial
Se conserva `buffalo_l` para compatibilidad con embeddings existentes. El modelo se carga de forma diferida y usa detección 320x320 por defecto para reducir arranque/CPU/RAM. Primer reconocimiento puede tardar más por la carga del modelo.

## Migraciones
Alembic queda configurado. Para una BD existente, revise primero `alembic revision --autogenerate -m "baseline"` antes de aplicar cambios. No ejecute migraciones destructivas sin revisar el SQL generado.

## Inicio
El Dockerfile usa `$PORT`, 1 worker y proxy headers compatibles con Railway.
