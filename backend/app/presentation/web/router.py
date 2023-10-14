from fastapi import APIRouter, HTTPException, status
from fastapi.responses import Response

from fastapi_cache.decorator import cache
from presentation.dependencies import container
from presentation.web.schemas import HealthResponse, HealthStatuses, Route
from schemas.atm import ATM
from schemas.office import Office
from shared.base import logger
from supplier.ort_supplier import RouteNotFound

router = APIRouter(prefix="")


@router.get("/health", response_model=HealthResponse, response_model_exclude_none=True)
async def check_server_health() -> HealthResponse:
    try:
        await container.heath_service.check()
    except Exception as exc:
        logger.exception("Exception while checking health")
        return HealthResponse(
            status=HealthStatuses.ERR, error=f"{exc.__class__.__name__}: {str(exc)}"
        )

    return HealthResponse(status=HealthStatuses.OK)


@router.get("/atms", response_model=list[ATM], response_model_exclude_none=True)
@cache(expire=60 * 5)
async def get_atms() -> list[ATM]:
    return await container.view_service.get_atms()


@router.get("/offices", response_model=list[Office], response_model_exclude_none=True)
@cache(expire=60 * 5)
async def get_offices() -> list[Office]:
    return await container.view_service.get_offices()


@router.post("/routes")
async def get_routes(route: Route) -> Response:
    """
    Returns GeoJson route between 2 points
    """
    try:
        result = await container.view_service.get_route(route.start, route.end)
    except RouteNotFound:
        raise HTTPException(
            detail="Route not found", status_code=status.HTTP_404_NOT_FOUND
        )
    return Response(content=result, headers={"Content-Type": "application/json"})
