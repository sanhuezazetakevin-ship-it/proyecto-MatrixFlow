from pathlib import Path


def test_dockerfile_uses_dynamic_port_and_one_worker():
    text = Path("Dockerfile").read_text(encoding="utf-8")
    assert "${PORT:-8080}" in text
    assert "--workers 1" in text
    assert "--proxy-headers" in text


def test_env_is_ignored():
    text = Path(".gitignore").read_text(encoding="utf-8")
    assert ".env" in text


def test_docker_context_excludes_secrets_and_venv():
    text = Path(".dockerignore").read_text(encoding="utf-8")
    assert ".env" in text
    assert ".venv" in text
