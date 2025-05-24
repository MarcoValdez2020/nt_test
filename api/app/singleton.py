from numeros import Numeros

# Creamos un singleton de la clase Numeros para que sea una unica instancia entre todas las peticiones
_numeros_instance = Numeros()

def get_numeros() -> Numeros:
    return _numeros_instance