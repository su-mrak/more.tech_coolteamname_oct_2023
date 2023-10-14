import enum
from dataclasses import dataclass

import aiohttp
from fastapi import status

from schemas.geo import Coordinate
from shared.settings import app_settings


class Profiles(str, enum.Enum):
    ...


class RouteNotFound(Exception):
    ...


@dataclass
class ORTSupplier:
    def __post_init__(self) -> None:
        self._baseurl = "https://api.openrouteservice.org/v2"
        self._headers = {
            "Authorization": app_settings.ort_apikey,
            "Accept": "application/json, application/geo+json, application/gpx+xml, img/png; charset=utf-8",
        }

    async def get_route(self, start: Coordinate, end: Coordinate) -> str:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                url=f"{self._baseurl}/directions/driving-car",
                params={
                    "start": start.to_str_tuple(),
                    "end": end.to_str_tuple(),
                    "api_key": app_settings.ort_apikey,
                },
            ) as res:
                if res.status == status.HTTP_404_NOT_FOUND:
                    raise RouteNotFound("Route not found")

                res.raise_for_status()
                return await res.text()
