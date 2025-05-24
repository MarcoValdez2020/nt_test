
from core.uow import UnitOfWork

def prueba():
    with UnitOfWork() as uow:
        # Aquí puedes usar los repositorios de la unidad de trabajo
        companies = uow.companies_repository.get_all_companies()
        print(companies)

if __name__ == "__main__":
    prueba()