import polars as pl
from datetime import date

from core.uow import UnitOfWork
from modules.companies.service import CompaniesService
from modules.charges.service import ChargesService

from modules.charges.models import ChargeStatus, Charges

today = date.today().strftime("%Y-%m-%d") # Obtenemos la fecha de hoy en formato YYYY-MM-DD

def cargar_companias_y_cargos():
    """ Carga las empresas y los cargos desde los archivos CSV a la base de datos. """
    
    print("****** Cargando empresas y cargos... ******")
    # Cargamos los datos en un dataframe de Polars
    data_df = pl.read_csv('data/data_prueba_tecnica.csv')
    # Limpiamos los nombres de las columnas
    data_df = data_df.rename({
        "id": "charge_id",
        "name": "company_name",
        "paid_at\r": "paid_at",  # Limpiamos el salto de línea al final de paid_at
    })

    print("DataFrame cargado con éxito.")
    
    print("Procesando cargos y compañias nuevas...")
    # Creamos un dataframe para las empresas agrupando por company_id y name dejando el nombre que aparece más veces
    # 1. Agrupamos por company_id y contamos las ocurrencias de cada nombre y cada id para mantener la combinación más frecuente en ambas columnas
    company_df = (
        data_df
        .select(pl.col("company_id"), pl.col("company_name"))  # Seleccionamos name y lo renombramos, y el company_id
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


    print("Procesando cargos...")
    # 2. Buscamos limpiar los cargos, filtrando los nulos, y guardar los en un archivo CSV para notificar que no se cargaron
    charges_null_df = (
        data_df
        .filter(pl.col("charge_id").is_null())  # Filtramos filas donde charge no es nulo
    )
    # Guardamos los cargos nulos en un archivo CSV
    if not charges_null_df.is_empty():
        charges_null_df.write_csv(f"generated_data/cargos_ids_nulos {today}.csv")
        print(f"Se encontraron {charges_null_df.height} cargos con ID nulos y se guardaron en 'generated_data/cargos_nulos {today}.csv'.")
    
    # 3. Como el df tiene nombres y companies_ids incorrectos, pero bien el almenos uno de los campos:
    # Los corrergiremos por medio de dos joins, para cuadrarlo con los nombres correctos y con los companies id_correctos

    
    # Preparamos dataframes específicamente para los joins
    company_df_id_join = company_df.select(
        pl.col("company_id"),
        pl.col("company_name").alias("company_name_by_id")
    )
    
    company_df_name_join = company_df.select(
        pl.col("company_id").alias("company_id_by_name"),
        pl.col("company_name")
    )

    # Realizamos los joins con columnas claramente nombradas
    charges_df = (
        data_df.filter(pl.col("charge_id").is_not_null())  # Filtramos filas donde charge no es nulo
        # Join por company_id para obtener company_name correcto
        .join(
            company_df_id_join,
            on="company_id",
            how="left"
        )
        # Join por name para obtener company_id correcto
        .join(
            company_df_name_join,
            on="company_name",
            how="left"
        )        # Aplicamos coalesce para tomar los valores correctos
        .with_columns([
            # Para company_id, preferimos el ID del join por name si existe,
            # de lo contrario mantenemos el original
            pl.coalesce(
                pl.col("company_id_by_name"),
                pl.col("company_id")
            ).alias("company_id_final"),
            
            # Para company_name, preferimos el nombre del join por id si existe,
            # de lo contrario usamos el name original
            pl.coalesce(
                pl.col("company_name_by_id"),
                pl.col("company_name")
            ).alias("company_name_final")
        ])
        # Seleccionamos solo las columnas que necesitamos con valores correctos
        .select(
            "charge_id",
            "amount", 
            "status", 
            "company_id_final",
            "company_name_final",
            "created_at",
            "paid_at"
        )
        # Renombramos las columnas finales para tener nombres limpios
        .rename({
            "company_id_final": "company_id",
            "company_name_final": "company_name"
        })
    )

    # Una vez correctos los nombres y ids procedemos a filtrar aquellos charges con con estatus validos
    # 4. Filtramos los cargos con estatus válidos creando una lista de estatus a partir de la clase definida en el modelo
    valid_statues  = [ statue.value for statue in ChargeStatus]

    # Obtener los registros que no tienen estatus valido y guardarlos en un CSV
    invalid_charges_df = (
        charges_df
        .filter(~pl.col("status").is_in(valid_statues))  # Filtramos filas donde status no está en los estatus válidos
    )

    if not invalid_charges_df.is_empty():
        # Guardamos los cargos inválidos en un archivo CSV
        invalid_charges_df.write_csv(f"generated_data/cargos_invalidos_estatus {today} .csv")
        print(f"Se encontraron {invalid_charges_df.height} cargos con estatus inválidos y se guardaron en 'generated_data/cargos_invalidos {today} .csv'.")
    
    # Filtrar solo los cargos con estatus válidos
    charges_df = (
        charges_df
        .filter(pl.col("status").is_in(valid_statues))  # Filtramos filas donde status está en los estatus válidos
    )


    # Limpiar las columnas de fechas eliminando los caracteres basura
    charges_df = (
        charges_df
        .with_columns([
            pl.col("created_at").str.strip_chars().alias("created_at"),
            pl.col("paid_at").str.strip_chars().alias("paid_at")
        ])
    )


    # Convertir la columna 'created_at'  y 'paid_at' a tipo fecha en formato YYYY-MM-DD
    charges_df = (
        charges_df
        .with_columns([
            parsear_fechas("created_at"),
            parsear_fechas("paid_at")
        ])
    )


    # Castear la columna amount para que sean decimales con formato 16,2, y ponemos strict=False para filtrar los registos que superen el formato
    # y los guardamos en un CSV
    charges_df = (
        charges_df
        .with_columns([
            pl.col("amount").cast(pl.Decimal(16, 2), strict=False).alias("amount")
        ])
    )

    # Crear un df con los cargos inválidos donde amount es nulo
    invalid_amount_df = (
        charges_df
        .filter(pl.col("amount").is_null())  # Filtramos filas donde amount no es nulo
    )

    # Evaluamos si el df de cargos inválidos tiene alguno por agrergar
    if not invalid_amount_df.is_empty():
        # Guardamos los cargos inválidos en un archivo CSV
        invalid_amount_df.write_csv(f"generated_data/cargos_invalidos_amount {today} .csv")
        print(f"Se encontraron {invalid_amount_df.height} cargos con amount inválido y se guardaron en 'generated_data/cargos_invalidos_amount {today} .csv'.")

    # Filtramos los cargos con amount válidos
    charges_df = (
        charges_df
        .filter(pl.col("amount").is_not_null())  # Filtramos filas donde amount no es nulo
    )

    print("DataFrame de cargos procesado con éxito, procediendo a guardar en la base de datos.")
    # 5. Guardamos los cargos válidos en la base de datos
    agregar_cargos_nuevos(charges_df)
    print("Carga de cargos completada.")




    



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


def parsear_fechas(col:str) -> pl.DataFrame:
    """ Limpia las fechas de un DataFrame. 
    Debido a que se encontraron fechas en diferentes formatos, se implementa una función para limpiar las fechas
    y convertirlas al formato YYYY-MM-DD.
    Se manejan tres casos:
        1. Formato YYYY-MM-DDTHH:MM:SS
        2. Formato YYYYMMDD
        3. Formato YYYY-MM-DD
    Args:
        col (str): Nombre de la columna a limpiar.
    Returns:
        pl.Expression: Expresión de Polars para limpiar la columna de fechas.
    """
    return  (
        pl.when(pl.col(col).is_null()) 
            .then(None) # Si la columna es nula, la dejamos como None
        .when(pl.col(col).str.contains("T")) # Evaluamos el formato YYYY-MM-DDTHH:MM:SS
            .then(pl.col(col).str.strptime(pl.Datetime, "%Y-%m-%dT%H:%M:%S", strict=False).dt.date()) # Convertimos a fecha
        .when(pl.col(col).str.len_chars() == 8) # Evaluamos el formato YYYYMMDD
            .then(pl.col(col).str.strptime(pl.Date, "%Y%m%d", strict=False)) # Convertimos a fecha
        .otherwise(pl.col(col).str.strptime(pl.Date, "%Y-%m-%d", strict=False)) # Si no es ninguno de los anteriores, asumimos que es YYYY-MM-DD
        .alias(col)
    )


def agregar_cargos_nuevos(charges_df: pl.DataFrame, chunk_size: int = 1000):
    """ Agrega nuevos cargos a la base de datos. 
    Args:
        charges_df (pl.DataFrame): DataFrame de Polars con los cargos a agregar.
    """
    # Instanciamos el servicio de cargos
    charges_service = ChargesService(UnitOfWork())

    
    columns_to_keep = list(Charges.model_fields.keys()) # Obtenemos los nombres de las columnas del modelo Charges
    charges_df = charges_df.select(columns_to_keep) # Seleccionamos solo las columnas que están en el modelo Charges

    # Llamamos al servicio para traer los cargos existentes
    existing_charges_df = charges_service.get_all_charges()

    # Si no hay cargos existentes, los insertamos todos
    if existing_charges_df.is_empty():
        print("No hay cargos existentes, insertando todos los nuevos.")
        # Dividimos el DataFrame en chunks para insertar en lotes
        for i in range(0, charges_df.height, chunk_size):
            chunk = charges_df[i:i+chunk_size]
            # Insertamos el chunk en la base de datos
            charges_service.create_charges_batch(chunk.to_dicts())
    else:
        # Filtramos los cargos que no están en la base de datos
        new_charges_df = charges_df.join(
            existing_charges_df.select("charge_id"),
            on="charge_id",
            how="anti"
        )
        
        # Si hay nuevos cargos, los insertamos
        if not new_charges_df.is_empty():
            print(f"Nuevos cargos a agregar: {new_charges_df.height} ")
            # Dividimos el DataFrame en chunks para insertar en lotes
            for i in range(0, new_charges_df.height, chunk_size):
                chunk = new_charges_df[i:i+chunk_size]
                charges_service.create_charges_batch(chunk.to_dicts())
        else:
            print("No hay nuevos cargos para agregar.")
    
    print("Proceso de cargos completado.")

if __name__ == "__main__":
    print("Iniciando la carga de empresas y cargos...")
    cargar_companias_y_cargos()
    print("Carga de empresas y cargos completada.")