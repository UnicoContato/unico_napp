from sqlalchemy import inspect, text

from app.extensions import db
from app import create_app
from app.models import *
from app.models.valores_atributos import ValoresAtributos

app = create_app()

with app.app_context():
    db.create_all()

    inspector = inspect(db.engine)
    if inspector.has_table("user"):
        existing_columns = {column["name"] for column in inspector.get_columns("user")}
        if "webhook_url" not in existing_columns:
            db.session.execute(text('ALTER TABLE "user" ADD COLUMN webhook_url VARCHAR(255)'))
            db.session.commit()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)