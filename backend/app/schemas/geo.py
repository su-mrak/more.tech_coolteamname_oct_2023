import uuid

from pydantic import Field

from schemas.base import CamelizedBaseModel


class Coordinate(CamelizedBaseModel):
    lat: float
    lng: float


class GeoObject(CamelizedBaseModel):
    id_: uuid.UUID = Field(..., alias="id")
    address: str = Field(
        ...,
        example="142000, Московская область, г. Домодедово, микрорайон Центральный, Каширское шоссе, д. 29",
    )
    coordinate: Coordinate = Field(
        ..., example=Coordinate(lat=55.478329, lng=37.298706)
    )
