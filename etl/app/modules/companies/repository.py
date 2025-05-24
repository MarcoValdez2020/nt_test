from sqlmodel import Session, insert, select
from typing import List

from modules.companies.models import Companies

class CompaniesRepository:
    """Clase para manejar operaciones CRUD en la tabla de cargos (charges) de la base de datos."""

    def __init__(self, session: Session):
        """Inicializa el repositorio con una sesión de base de datos."""
        self.session = session

    def get_all_companies(self) -> List[Companies]:
        """Obtiene todas las empresas de la base de datos.
        Returns:
            List[Companies]: Lista de objetos Companies.
        """
        statement = select(Companies)
        result = self.session.execute(statement)
        if result is None:
            return []
        return result.scalars().fetchall()
    
    def get_company_by_id(self, company_id: str) -> Companies:
        """Obtiene una empresa específica por su ID.
        Args:
            company_id (str): ID de la empresa.
        Returns:
            Companies: Objeto Companies correspondiente al ID proporcionado.
        """
        statement = select(Companies).where(Companies.company_id == company_id)
        result = self.session.execute(statement)
        return result.scalars().first()
    
    def create_companies_batch(self, companies: List[dict]) -> bool:
        """Función para insertar companies por lotes
        Args:
            companies (List[dict]): Lista de companies a insertar.
        Returns:
            bool: True si la operación fue exitosa.
        """
        
        # Insertar las ventas en la base de datos
        statement = insert(Companies).values(companies)
        self.session.execute(statement)
        print(f'Lote de {len(companies)} empresas insertadas correctamente.')

        return True