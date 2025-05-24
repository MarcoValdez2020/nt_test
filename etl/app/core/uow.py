
from typing import Callable
from sqlalchemy.orm import Session

from core.db_connection import DbFactoryConnection, db_factory_connection
from modules.charges.repository import ChargesRepository
from modules.companies.repository import CompaniesRepository

class UnitOfWork():
    """Clase base para la unidad de trabajo (UoW) que maneja la sesión de base de datos y los repositorios."""

    def __init__(self, session_factory:  DbFactoryConnection = db_factory_connection):
        """ Inicializa la unidad de trabajo con la fábrica de sesiones pero no la sesión"""
        self.session_factory = session_factory
        self.session: Session = None  
        self.companies_repository: CompaniesRepository = None
        self.charges_repository: ChargesRepository = None


    def __enter__(self):
        """Inicia la sesión de base de datos y los repositorios."""
        # Inicia la sesión de base de datos y los repositorios
        self.session = self.session_factory.create_session()

        # Inicializa los repositorios
        self.companies_repository = CompaniesRepository(self.session)
        self.charges_repository = ChargesRepository(self.session)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Maneja el cierre de la sesión de base de datos, haciendo commit si no hay errores o rollback en caso contrario.
        
        Args:
            exc_type: Tipo de excepción (si ocurrió).
            exc_value: Instancia de la excepción.
            traceback: Información del traceback.
        """
        try:
            if self.session is None:
                print("Advertencia: No hay sesión activa para cerrar.")
                return

            if exc_type is None:
                self.session.commit()
            else:
                print(f"Error detectado: {exc_type.__name__}: {exc_value}. Revirtiendo transacción...")
                self.session.rollback()


        except Exception as inner_exc:
            print(f"Error inesperado al cerrar la sesión: {inner_exc}. Forzando rollback...")
            if self.session.is_active:
                self.session.rollback()
            
        finally:
            if hasattr(self, 'session') and self.session is not None:
                self.session.close()


    def commit(self):
        """Permite confirmar manualmente los cambios si es necesario"""
        self.session.commit()

    def rollback(self):
        """Revierte manualmente la transacción si hay un error"""
        self.session.rollback()
