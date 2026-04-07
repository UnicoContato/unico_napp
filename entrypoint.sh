#!/bin/sh

echo "⏳ Aguardando banco subir..."

while ! nc -z db 5432; do
  sleep 1
done

echo "✅ Banco pronto!"

echo "📦 Criando tabelas..."

python run.py