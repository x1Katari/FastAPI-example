from typing import Dict, List

from pydantic import BaseModel


class CargoIn_Pydantic(BaseModel):
    cargo_type: str
    rate: float
    class Config:
        orm_mode = True


class Cargo_Pydantic(BaseModel):
    id: int
    cargo_type: str
    rate: float
    class Config:
        orm_mode = True
        
class CargoRate(BaseModel):
    cargo_type: str
    rate: str

class CargoRates(BaseModel):
    cargo_rates: Dict[str, List[CargoRate]]