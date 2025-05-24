import os
from dotenv import load_dotenv

# Clase para cargar la configuración de la base de datos
class BdConfig:
    def __init__(self):
        self.db_host = os.getenv("POSTGRES_CONTAINER_NAME") # No se usa el host porque esta en distinto contendor, usamos su nombre porque tiene su ip
        self.db_port = 5432 # Puerto del contenedor de postgres, se pone el default porque al interconectar los contenedores no se usa el puerto del host
        self.db_user = os.getenv("POSTGRES_USER")
        self.db_password = os.getenv("POSTGRES_PASSWORD")
        self.db_name = os.getenv("POSTGRES_DB")


    def get_connection_string(self):
        return f"postgresql://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"