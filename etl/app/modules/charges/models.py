from datetime import date
from sqlmodel import SQLModel, Field, Relationship
from typing import TYPE_CHECKING
from decimal import Decimal
from enum import Enum


if TYPE_CHECKING:
    from modules.companies.models import Companies

# Creamos un enum con los estados posibles de un cargo
class ChargeStatus(str, Enum):
    voided = 'voided'
    pending_payment = 'pending_payment'
    paid = 'paid'
    pre_authorized = 'pre_authorized'
    refunded = 'refunded'
    charged_back = 'charged_back'
    expired = 'expired'
    partially_refunded = 'partially_refunded'

class Charges(SQLModel, table=True):
    __tablename__ = "charges"

    charge_id: str = Field(primary_key=True, max_length=40, nullable=False)
    company_id: str = Field(max_length=40, nullable=False, foreign_key='companies.company_id')
    amount: Decimal = Field(default=0, max_digits=16, decimal_places=2, nullable=False)
    status: ChargeStatus = Field(default=None, nullable=False)
    created_at: date = Field(default=date.today())
    paid_at: date = Field(default=None, nullable=True)
    
    
    company: "Companies" = Relationship(back_populates="charges")