from fastapi import APIRouter
from presentation.web.schemas import HealthResponse, HealthStatuses
from presentation.dependencies import container
from shared.base import logger

router = APIRouter(prefix="")


@router.get("/health", response_model=HealthResponse, response_model_exclude_none=True)
async def check_server_health() -> HealthResponse:
    try:
        await container.heath_service.check()
    except Exception as exc:
        logger.exception("Exception while checking health")
        return HealthResponse(status=HealthStatuses.ERR, error=f"{exc.__class__.__name__}: {str(exc)}")

    return HealthResponse(status=HealthStatuses.OK)
