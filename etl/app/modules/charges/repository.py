from sqlmodel import Session, insert, select
from typing import List

from modules.charges.models import Charges

class ChargesRepository:
    """Clase para manejar operaciones CRUD en la tabla de cargos (charges) de la base de datos."""

    def __init__(self, session: Session):
        """Inicializa el repositorio con una sesión de base de datos."""
        self.session = session

    def get_all_charges(self) -> List[Charges]:
        """Obtiene todos los cargos de la base de datos.
        Returns:
            List[Charges]: Lista de objetos Charges.
        """
        statement = select(Charges)
        result = self.session.execute(statement)
        if result is None:
            return []
        return result.scalars().fetchall()

    def get_charge_by_id(self, charge_id: str) -> Charges:
        """Obtiene un cargo específico por su ID.
        Args:
            charge_id (str): ID del cargo.
        Returns:
            Charges: Objeto Charges correspondiente al ID proporcionado.
        """
        statement = select(Charges).where(Charges.charge_id == charge_id)
        result = self.session.execute(statement)
        return result.scalars().first()
    
    def get_charges_by_company_id(self, company_id: str) -> List[Charges]:
        """Obtiene todos los cargos de una empresa específica por su ID.
        Args:
            company_id (str): ID de la empresa.
        Returns:
            List[Charges]: Lista de cargos asociados a la empresa.
        """
        statement = select(Charges).where(Charges.company_id == company_id)
        result = self.session.execute(statement)
        if result is None:
            return []
        return result.scalars().fetchall()
    
    def create_charges_batch(self, charges: List[dict]) -> bool:
        """Función para insertar charges por lotes
        Args:
            charges (List[dict]): Lista de charges a insertar.
        Returns:
            bool: True si la operación fue exitosa.
        """
        
        # Insertar las cargos en la base de datos
        statement = insert(Charges).values(charges)
        self.session.execute(statement)
        print(f'Lote de {len(charges)} cargos insertadas correctamente.')

        return True
