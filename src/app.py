import json
from datetime import datetime, date

from fastapi import FastAPI, HTTPException, UploadFile, File, Query
from tortoise.contrib.fastapi import register_tortoise, HTTPNotFoundError

import settings
from src.models import Cargo
from typing import List, Optional

from src.schemas import Cargo_Pydantic, CargoIn_Pydantic

app = FastAPI()


@app.get('/cargos', response_model=List[Cargo_Pydantic])
async def get_cargos():
    cargos = await Cargo.all()
    return [Cargo_Pydantic(**cargo.__dict__) for cargo in cargos]


@app.post("/upload_cargo_rates")
async def upload_cargo_rates(file: UploadFile = File(...)):
    try: 
        if file.filename.endswith('.json'):
            contents = await file.read()
            data = json.loads(contents)
        else:
            raise HTTPException(status_code=400, detail="Invalid file type. Please upload a .json file.")

        for upd_date, cargo_list in data.items():
            for cargo in cargo_list:
                cargo_type = cargo.get("cargo_type")
                rate = float(cargo.get("rate"))

                date_dt = date.fromisoformat(upd_date)

                await Cargo.create(cargo_type=cargo_type, rate=rate,
                                   modified_at=datetime(date_dt.year, date_dt.month, date_dt.day))
        return {"status": 200, "detail": "success"}
    except:
        return {"status": 400, "detail": "incorrect file"}


@app.post("/cargos", response_model=Cargo_Pydantic)
async def create_or_update_cargo(cargo: CargoIn_Pydantic):
    cargo_obj = await Cargo.get_or_none(cargo_type=cargo.cargo_type)
    if cargo_obj:
        cargo_obj = await Cargo.create(**cargo.dict(exclude_unset=True), modified_at=datetime.now())
    else:
        cargo_obj = await Cargo.create(**cargo.dict(exclude_unset=True), modified_at=datetime.now())

    return Cargo_Pydantic(**cargo_obj.__dict__)


@app.get('/insurance_cost')
async def get_insurance_cost(cargo_type: str, declared_value: float, date: str =""):
    date_dt = datetime.strptime(date, '%Y-%m-%d') if date else None
    if date_dt:
        cargo_obj = await Cargo.filter(cargo_type=cargo_type, modified_at__lte=date_dt).order_by('-modified_at').first()
    else:
        cargo_obj = await Cargo.filter(cargo_type=cargo_type).order_by('-modified_at').first()

    if not cargo_obj:
        return HTTPException(status_code=404, detail="No cargo rate found for provided cargo type and date")

    insurance_cost = cargo_obj.rate * declared_value
    return {"insurance_cost": insurance_cost}


@app.post("/upload_cargo_rates")
async def upload_cargo_rates(file: UploadFile = File(...)):
    try: 
        if file.filename.endswith('.json'):
            contents = await file.read()
            data = json.loads(contents)
        else:
            raise HTTPException(status_code=400, detail="Invalid file type. Please upload a .json file.")
    
        for upd_date, cargo_list in data.items():
            for cargo in cargo_list:
                cargo_type = cargo.get("cargo_type")
                rate = float(cargo.get("rate"))
                db_cargo = await Cargo.get_or_none(cargo_type=cargo_type)
    
                date_dt = date.fromisoformat(upd_date)
    
                if db_cargo:
                    db_cargo.rate = rate
                    db_cargo.modified_at = datetime(date_dt.year, date_dt.month, date_dt.day)
                    await db_cargo.save()
                else:
                    await Cargo.create(cargo_type=cargo_type, rate=rate,
                                       created_at=datetime(date_dt.year, date_dt.month, date_dt.day))
        return {"status": 200, "detail": "succes"}
    except:
        return {"status": 500, "detail": "uncorrect file"}
    
    
@app.get("/cargo_history/{cargo_type}", response_model=List[Cargo_Pydantic])
async def get_cargo_history(cargo_type: str, 
                            start_date: Optional[str] = Query(None, regex="^(\d{4})-(\d{2})-(\d{2})$"),
                            end_date: Optional[str] = Query(None, regex="^(\d{4})-(\d{2})-(\d{2})$")):
    try:
        if start_date:
            start_date_dt = datetime.strptime(start_date, '%Y-%m-%d')
        else:
            start_date_dt = None

        if end_date:
            end_date_dt = datetime.strptime(end_date, '%Y-%m-%d')
        else:
            end_date_dt = None

    except ValueError as ve:
        return HTTPException(status_code=400, detail="Invalid date format. Expected YYYY-MM-DD")

    if start_date_dt and end_date_dt and start_date_dt > end_date_dt:
        raise HTTPException(status_code=400, detail="Start date should be less than the end date")

    if start_date_dt and end_date_dt:
        cargo_obj_list = await Cargo.filter(
            cargo_type=cargo_type, modified_at__gte=start_date_dt, modified_at__lte=end_date_dt).order_by('-modified_at').all()
    elif start_date_dt:
        cargo_obj_list = await Cargo.filter(
            cargo_type=cargo_type, modified_at__gte=start_date_dt).order_by('-modified_at').all()        
    elif end_date_dt:
        cargo_obj_list = await Cargo.filter(
            cargo_type=cargo_type, modified_at__lte=end_date_dt).order_by('-modified_at').all()
    else:
        cargo_obj_list = await Cargo.filter(cargo_type=cargo_type).order_by('-modified_at').all()

    if not cargo_obj_list:
        raise HTTPException(status_code=404, detail=f"No cargo rate history found for {cargo_type}")

    return [Cargo_Pydantic(**cargo.__dict__) for cargo in cargo_obj_list]


register_tortoise(
    app,
    config=settings.DATABASE_CONFIG,
    generate_schemas=True,
)
