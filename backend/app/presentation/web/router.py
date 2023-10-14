import enum
import uuid

from fastapi import APIRouter, HTTPException, status
from fastapi.responses import Response

from fastapi_cache.decorator import cache
from presentation.dependencies import container
from presentation.web.schemas import (
    HealthResponse,
    HealthStatuses,
    Route,
    RouteByTeller,
    TopTellersResponse,
)
from schemas.atm import ATM
from schemas.office import Office
from schemas.search import GetTopTellers
from service.view_service import TellerNotFound
from shared.base import logger
from supplier.ort_supplier import RouteNotFound

router = APIRouter(prefix="")


class Tags(str, enum.Enum):
    SERVICE = "service"
    ROUTE = "route"
    TELLERS = "tellers"


@router.get(
    "/health",
    response_model=HealthResponse,
    response_model_exclude_none=True,
    tags=[Tags.SERVICE],
)
async def check_server_health() -> HealthResponse:
    try:
        await container.heath_service.check()
    except Exception as exc:
        logger.exception("Exception while checking health")
        return HealthResponse(
            status=HealthStatuses.ERR, error=f"{exc.__class__.__name__}: {str(exc)}"
        )

    return HealthResponse(status=HealthStatuses.OK)


@router.get(
    "/atms",
    response_model=list[ATM],
    response_model_exclude_none=True,
    tags=[Tags.TELLERS],
)
@cache(expire=60 * 5)
async def get_atms() -> list[ATM]:
    return await container.view_service.get_atms()


@router.get(
    "/offices",
    response_model=list[Office],
    response_model_exclude_none=True,
    tags=[Tags.TELLERS],
)
@cache(expire=60 * 5)
async def get_offices() -> list[Office]:
    return await container.view_service.get_offices()


@router.post("/routes", tags=[Tags.ROUTE])
async def get_routes(route: Route) -> Response:
    """
    Returns GeoJson route between 2 points
    """
    try:
        result = await container.view_service.get_route(
            route.start, route.end, profile=route.profile
        )
    except RouteNotFound:
        raise HTTPException(
            detail="Route not found", status_code=status.HTTP_404_NOT_FOUND
        )
    return Response(content=result, headers={"Content-Type": "application/json"})


@router.post("/routes/by-teller", tags=[Tags.ROUTE])
async def get_routes_by_teller(route: RouteByTeller) -> Response:
    """
    Returns GeoJson route between start point and desired teller(ATM of Office)
    """
    try:
        result = await container.view_service.get_route_by_id(
            route.start,
            teller_id=route.teller_id,
            teller_type=route.teller_type,
            profile=route.profile,
        )
    except RouteNotFound:
        raise HTTPException(
            detail="Route not found", status_code=status.HTTP_404_NOT_FOUND
        )
    except TellerNotFound:
        raise HTTPException(
            detail="Teller not found", status_code=status.HTTP_404_NOT_FOUND
        )
    return Response(content=result, headers={"Content-Type": "application/json"})


@router.post("/tellers", response_model=TopTellersResponse, tags=[Tags.TELLERS])
async def get_top_teller_filtered(
    top_tellers_request: GetTopTellers,
) -> TopTellersResponse:
    atms, offices = await container.view_service.get_top_teller_filtered(
        top_tellers_request=top_tellers_request
    )
    return TopTellersResponse(atms=atms, offices=offices)


@router.post("/tap")
async def confirm_tap(tellerId: uuid.UUID, typperType: str) -> None:
    return None
