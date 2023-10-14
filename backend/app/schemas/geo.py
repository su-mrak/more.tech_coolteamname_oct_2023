import uuid

from pydantic import Field

from schemas.base import CamelizedBaseModel


class Coordinate(CamelizedBaseModel):
    lat: float
    lng: float

    def to_str_tuple(self) -> str:
        return f"{self.lng},{self.lat}"


class Metro(CamelizedBaseModel):
    distance: float
    name: str
    line: str


class GeoObject(CamelizedBaseModel):
    id_: uuid.UUID = Field(..., alias="id")
    address: str = Field(
        ...,
        example="142000, Московская область, г. Домодедово, микрорайон Центральный, Каширское шоссе, д. 29",
    )
    coordinate: Coordinate = Field(
        ..., example=Coordinate(lat=55.478329, lng=37.298706)
    )
    load: int = Field(3, example=1)
    duration_walk: float | None = Field(None, example=20)  # Minutes
    duration_car: float | None = Field(None, example=5)  # Minutes
    distance: float | None = Field(None, example=430)  # Metre
    closest_metro: Metro | None = None
