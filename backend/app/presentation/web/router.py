from fastapi import APIRouter
from presentation.web.schemas import HealthResponse, HealthStatuses

router = APIRouter(prefix="")


@router.get("/health", response_model=HealthResponse, response_model_exclude_none=True)
async def check_server_health() -> HealthResponse:
    return HealthResponse(status=HealthStatuses.OK)
