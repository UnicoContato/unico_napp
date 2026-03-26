#!/bin/sh

echo "⏳ Aguardando banco subir..."

while ! nc -z db 5432; do
  sleep 1
done

echo "✅ Banco pronto!"

echo "🚀 Rodando migrations..."
alembic upgrade head

echo "🔥 Subindo API..."
python run.py
