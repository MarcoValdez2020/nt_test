import polars as pl

from core.uow import UnitOfWork
from modules.companies.service import CompaniesService
from modules.charges.service import ChargesService


def cargar_companias_y_cargos():
    """ Carga las empresas y los cargos desde los archivos CSV a la base de datos. """
    
    print("****** Cargando empresas y cargos... ******")
    # Cargamos los datos en un dataframe de Polars
    data_df = pl.read_csv('data/data_prueba_tecnica.csv')
    print("DataFrame cargado con éxito.")
    
    print("Procesando cargos y compañias nuevas...")
    # Creamos un dataframe para las empresas agrupando por company_id y name dejando el nombre que aparece más veces
    # 1. Agrupamos por company_id y contamos las ocurrencias de cada nombre y cada id para mantener la combinación más frecuente en ambas columnas
    company_df = (
        data_df
        .select(pl.col("company_id"), pl.col("name").alias("company_name"))  # Seleccionamos name y lo renombramos, y el company_id
        .filter(pl.col("company_id").is_not_null())  # Filtramos filas donde company_id no es nulo
        .filter(pl.col("company_name").is_not_null())  # Filtramos filas donde name no es nulo
        .group_by("company_id", "company_name")  # Agrupa por ambas columnas
        .agg(pl.len().alias("count"))         # Cuenta ocurrencias de cada combinación entre company_id y company_name
        .sort("count", descending=True)         # Ordena de mayor a menor conteo
        .unique("company_id", keep="first")     # Conserva el nombre más frecuente
        .sort("count", descending=True)         # Ordenamos porque el uniquie no mantiene el orden
        .unique("company_name", keep="first")     # Conserva el nombre más frecuente
        .drop("count")                          # Eliminamos la columna de conteo
    )

    print("DataFrame de compañías procesado con éxito.")
    # Agregramos las empresas a la base de datos
    agregar_companias_nuevas(company_df)



    
def agregar_companias_nuevas(company_df: pl.DataFrame):
    """ Agrega nuevas empresas a la base de datos. 
    Args:
        company_df (pl.DataFrame): DataFrame de Polars con las empresas a agregar.
    """
    print("Verificando si hay compañias nuevas para agregar...")
    # Instanciamos el servicio de compañías
    companies_service = CompaniesService(UnitOfWork())

    # Llamamos al servicio para traer las compañías existentes
    existing_companies_df = companies_service.get_all_companies()

    # Si no hay compañías existentes, las insertamos todas
    if existing_companies_df.is_empty():
        companies_service.create_companies_batch(company_df.to_dicts())
    else:
        # Filtramos las compañías que no están en la base de datos
        new_companies_df = company_df.join(
            existing_companies_df.select("company_id"),
            on="company_id",
            how="anti"
        )
        
        # Si hay nuevas compañías, las insertamos
        if not new_companies_df.is_empty():
            print(f"Nuevas compañías a agregar: {new_companies_df.height} ")
            companies_service.create_companies_batch(new_companies_df.to_dicts())
        else:
            print("No hay nuevas compañías para agregar.")
    
    print("Proceso de compañías completado.")




if __name__ == "__main__":
    print("Iniciando la carga de empresas y cargos...")
    cargar_companias_y_cargos()
    print("Carga de empresas y cargos completada.")