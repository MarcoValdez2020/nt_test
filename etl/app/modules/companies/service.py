import polars as pl
from core.uow import UnitOfWork

class CompaniesService:
    """ Servicio para manejar las operaciones relacionadas con las empresas. """
    
    def __init__(self, uow: UnitOfWork):
        self.uow = uow  # Inyectar la unidad de trabajo (UnitOfWork)

    def get_all_companies(self) -> pl.DataFrame:
        """ Obtiene todas las empresas. 
        Returns:
            pl.DataFrame: DataFrame de Polars con todas las empresas.
        """
        with self.uow as uow:
            companies = uow.companies_repository.get_all_companies()
            if not companies:
                return pl.DataFrame()
        return pl.DataFrame([company.model_dump() for company in companies])
    
    def get_company_by_id(self, company_id: str) -> pl.DataFrame:
        """ Obtiene una empresa por su ID. 
        Args:
            company_id (str): ID de la empresa a buscar.
        Returns:
            pl.DataFrame: DataFrame de Polars con la empresa encontrada, o un DataFrame vacío si no se encuentra.
        """
        with self.uow as uow:
            company = uow.companies_repository.get_company_by_id(company_id)
            if not company:
                return pl.DataFrame()
        return pl.DataFrame([company.model_dump()])
    
    def create_companies_batch(self, companies: list[dict]) -> bool:
        """ Inserta un lote de empresas en la base de datos. 
        Args:
            companies (list[dict]): Lista de empresas a insertar.
        Returns:
            bool: True si la operación fue exitosa.
        """
        with self.uow as uow:
            success = uow.companies_repository.create_companies_batch(companies)
        return success