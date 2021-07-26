from logger import log_settings
from typing import Optional
from fastapi import FastAPI, Request, Response, APIRouter
from typing import List
from starlette.middleware.cors import CORSMiddleware
from models.model_mysql import *
import traceback
import logging
logger = logging.getLogger(__name__)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup():
    logger.info("##### startup. #####")


@app.middleware("http")
def http_add_log(request: Request, call_next):
    try:
        logger.info("[RequestUrl] " + request.url.path)
        logger.info("[RequestHost] " + request.client.host)
        result = call_next(request)
        return result
    except Exception as e:
        logger.error(traceback.format_exc())
        return Response("internal server error", status_code=500, headers=None, media_type='text/plain')


# 車両一覧 (ページネーション有)
@app.get("/api/vehicle-list")
def vehicle_list(
    limit: int,
    offset: int,
    maker_id: Optional[int] = None,
    car_id: Optional[int] = None,
    price: Optional[int] = None,
    model_year: Optional[str] = None,
    mileage: Optional[int] = None,
    unrunnable: Optional[bool] = False,
    displacement: Optional[int] = None,
    vehicle_inspection_expiry: Optional[int] = None
):
    return get_vehicle_list(
        limit=limit,
        offset=offset,
        maker_id=maker_id,
        car_id=car_id,
        price=price,
        model_year=model_year,
        mileage=mileage,
        unrunnable=unrunnable,
        displacement=displacement,
        vehicle_inspection_expiry=vehicle_inspection_expiry
    )


# グラフ用データ(走行距離別、1万km単位で集計、平均値)
@app.get("/api/vehicle-graph")
def vehicle_graph(car_id: int):
    return get_vehicle_graph(car_id=car_id)
