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
    maker_id: Optional[int] = None,
    car_id: Optional[int] = None,
    price: Optional[int] = None,
    model_year: Optional[str] = None,
    mileage: Optional[int] = None,
    unrunnable: Optional[bool] = False,
    displacement: Optional[int] = None,
    vehicle_inspection_expiry: Optional[int] = None,
    limit: Optional[int] = 1,
    offset: Optional[int] = 0,
):

    return get_vehicle_list(
        maker_id=maker_id,
        car_id=car_id,
        price=price,
        model_year=model_year,
        mileage=mileage,
        unrunnable=unrunnable,
        displacement=displacement,
        vehicle_inspection_expiry=vehicle_inspection_expiry,
        limit=limit,
        offset=offset
    )

# グラフ用データ(走行距離別、1万km単位で集計、平均値)


# @app.get("/api/vehicle-graph")
# def vehicle_list(
#     maker_id: int, car_id: int, price: int, model_year: str,
#     mileage: int, unrunnable: bool, displacement: int,
#     vehicle_inspection_expiry: int
# ):
#     users = session.query(UserTable).all()
#     return users


# @app.get("/users")
# def read_users():
#     users = session.query(UserTable).all()
#     time.sleep(3)
#     return users


# @app.get("/users/{user_id}")
# def read_user(user_id: int):
#     user = session.query(UserTable).\
#         filter(UserTable.id == user_id).first()
#     return user


# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: str = None):
#     return {"item_id": item_id, "q": q}
