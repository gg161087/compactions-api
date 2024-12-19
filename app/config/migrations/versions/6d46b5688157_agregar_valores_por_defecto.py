"""Agregar valores por defecto

Revision ID: 6d46b5688157
Revises: 
Create Date: 2024-11-26 20:24:07.507951

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import os
import sys


# revision identifiers, used by Alembic.
revision: str = '6d46b5688157'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

SEED_FILE = os.path.join(os.path.dirname(__file__), '../../../seed/distritos_seed.py')


def upgrade() -> None:
    distritos = _cargar_distritos()

    # Realizar inserciones en la tabla
    conn = op.get_bind()
    for distrito in distritos:
        conn.execute(
            sa.text("INSERT INTO distritos (renglon, municipio) VALUES (:renglon, :municipio)"),
            {"renglon": distrito["renglon"], "municipio": distrito["municipio"]}
        )


def downgrade():
    # Borrar los datos iniciales (opcional)
    op.execute("DELETE FROM distritos")

def _cargar_distritos():
    # Asegurar que podemos importar distritos.py
    sys.path.insert(0, os.path.abspath(os.path.join(SEED_FILE, "../..")))
    from app.seed.distritos_seed import distritos
    return distritos