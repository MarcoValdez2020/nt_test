import polars as pl

from core.uow import UnitOfWork

class ChargesService:
    """ Servicio para manejar las operaciones relacionadas con los cargos. """
    def __init__(self, uow: UnitOfWork):
        self.uow = uow # Inyectar la unidad de trabajo (UnitOfWork)

    def get_all_charges(self) -> pl.DataFrame:
        """ Obtiene todos los cargos. 
        Returns:
            pl.DataFrame: DataFrame de Polars con todos los cargos.
        """
        with self.uow as uow:
            # Aquí puedes usar los repositorios de la unidad de trabajo
            charges = uow.charges_repository.get_all_charges()
            if not charges:
                return pl.DataFrame()
        return pl.DataFrame([charge.model_dump() for charge in charges])
    
    def get_charge_by_id(self, charge_id: str) -> pl.DataFrame:
        """ Obtiene un cargo por su ID. 
        Args:
            charge_id (str): ID del cargo a buscar.
        Returns:
            pl.DataFrame: DataFrame de Polars con el cargo encontrado, o un DataFrame vacío si no se encuentra.
        """
        with self.uow as uow:
            charge = uow.charges_repository.get_charge_by_id(charge_id)
            if not charge:
                return pl.DataFrame()
        return pl.DataFrame([charge.model_dump()])
    
    def get_charges_by_company_id(self, company_id: str) -> pl.DataFrame:
        """ Obtiene los cargos asociados a una empresa por su ID. 
        Args:
            company_id (str): ID de la empresa.
        Returns:
            pl.DataFrame: DataFrame de Polars con los cargos asociados a la empresa, o un DataFrame vacío si no se encuentran.
        """
        with self.uow as uow:
            charges = uow.charges_repository.get_charges_by_company_id(company_id)
            if not charges:
                return pl.DataFrame()
        return pl.DataFrame([charge.model_dump() for charge in charges])
    

    def create_charges_batch(self, charges: list[dict]) -> bool:
        """ Inserta un lote de cargos en la base de datos. 
        Args:
            charges (list[dict]): Lista de cargos a insertar.
        Returns:
            bool: True si la operación fue exitosa.
        """
        with self.uow as uow:
            success = uow.charges_repository.create_charges_batch(charges)
        return success