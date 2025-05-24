from datetime import date
from sqlmodel import SQLModel, Field, Relationship
from typing import List, TYPE_CHECKING

if TYPE_CHECKING: # Importamos el typechecking para evitar problemas de referencia circular
    from modules.charges.models import Charges

class Companies(SQLModel, table=True):
    __tablename__ = "companies"

    company_id: str = Field(primary_key=True, max_length=40, nullable=False)
    company_name: str = Field(max_length=130, nullable=False)
    created_at: date = Field(default=date.today())


    charges: List["Charges"] = Relationship(back_populates="company")


from modules.charges.models import Charges # Importar Charges después de definir Companies para evitar problemas de referencia circular