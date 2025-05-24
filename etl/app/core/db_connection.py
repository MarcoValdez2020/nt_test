from sqlmodel import create_engine
from sqlalchemy.orm import sessionmaker

from core.config import bd_config

class DbFactoryConnection:
    """Clase para crear la conexión a la base de datos y proporcionar una sesión para interactuar con ella"""
    
    def __init__(self, url: str):
        self.engine = create_engine(
            url,
            future=True,
            pool_pre_ping=True, # Verificamos si la conexión está viva antes de usarla
            pool_recycle=3600, # Reciclamos conexiones cada 3600 segundos
            pool_size=10, # Tamaño del pool de conexiones 
        )
        self.SessionLocal = sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
            future=True
        )

    def create_session(self):
        return self.SessionLocal() # Se retorna una nueva sesión de la base de datos pues el uow se encarga de gestionar la sesión

# Creamos una instancia de la clase DbFactoryConnection para usar en el resto de la aplicación
db_factory_connection = DbFactoryConnection(bd_config.get_connection_string())