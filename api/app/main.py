from pydantic import BaseModel, Field
from fastapi import FastAPI, Depends, HTTPException

from numeros import Numeros
from singleton import get_numeros


app = FastAPI(
    title="API de Número Faltante",
    description="Permite extraer un número de una lista del 1 al 100 y calcular cuál fue eliminado.",
)

# Creacion de nuestro modelo de resquest
class ExtraerNumeroRequest(BaseModel):
    """Modelo de entrada para extraer un número"""
    numero: int = Field(..., description="Número a extraer (entre 1 y 100)", example=42)

# Creación de nuestra respuesta
class ExtraerNumeroResponse(BaseModel):
    """Respuesta para extracción de número"""
    mensaje: str = Field(..., description="Mensaje de éxito o error", example="Número extraído correctamente: 42")



# Definición de rutas

@app.get("/", summary="Página de bienvenida", description="Ruta por defecto del API")
def root():
    return {
        "mensaje": "Bienvenido a la API de Número Faltante",
        "descripcion": "Esta API permite extraer un número entre 1 y 100 y calcular el número extraído.",
        "link_de_documentacion": "http://localhost:8000/docs"
    }

@app.post(
    "/extraer-numero",
    response_model=ExtraerNumeroResponse,
    summary="Extraer el número que recibe como parámetro, de la lista",
    description="Extrae un número del conjunto de 1 a 100. Solo se puede extraer un número."
)
def extraer_numero(
    request: ExtraerNumeroRequest,
    numeros: Numeros = Depends(get_numeros)
):
    """
    Extrae un número de la lista interna. Solo se permite una extracción de todo el conjunto.
    """
    try:
        mensaje = numeros.extraer_numero(request.numero)
        return {"mensaje": mensaje}
    except (ValueError, TypeError) as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get(
    "/calcular-numero-extraido",
    summary="Calcular el número faltante de la lista",
    description="Devuelve el número que ha sido extraído del conjunto si existe."
)
def calcular_numero_extraido(numeros: Numeros = Depends(get_numeros)):
    """
    Calcula el número faltante basado en la diferencia del conjunto original.
    """
    try:
        numero = numeros.calcular_numero_extraido()
        return {"numero_extraido": numero}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post(
    "/reiniciar",
    summary="Reiniciar lista",
    description="Reinicia la lista a los números del 1 al 100."
)
def reiniciar(numeros: Numeros = Depends(get_numeros)):
    """
    Restaura la lista original del 1 al 100.
    """
    mensaje = numeros.reiniciar()
    return {"mensaje": mensaje}
