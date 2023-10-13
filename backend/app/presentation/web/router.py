from datetime import time

from fastapi import APIRouter

from fastapi_cache.decorator import cache
from presentation.dependencies import container
from presentation.web.schemas import HealthResponse, HealthStatuses
from schemas.atm import ATM, ServiceConfiguration, Services
from schemas.geo import Coordinate
from schemas.office import Office, OpenHours, Weekdays
from shared.base import logger

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
    import uuid

    return [
        ATM(
            id=uuid.uuid4(),
            address="AAA",
            coordinate=Coordinate(lat=55, lng=37),
            all_day=False,
            services=Services(
                blind=ServiceConfiguration(
                    service_activity=True, service_capability=False
                ),
                nfc_for_bank_cards=ServiceConfiguration(
                    service_activity=True, service_capability=False
                ),
                qr_read=ServiceConfiguration(
                    service_activity=True, service_capability=False
                ),
                supports_charge_rub=ServiceConfiguration(
                    service_activity=True, service_capability=False
                ),
                supports_eur=ServiceConfiguration(
                    service_activity=True, service_capability=False
                ),
                supports_rub=ServiceConfiguration(
                    service_activity=True, service_capability=False
                ),
                supports_usd=ServiceConfiguration(
                    service_activity=True, service_capability=False
                ),
                wheelchair=ServiceConfiguration(
                    service_activity=True, service_capability=False
                ),
            ),
        )
    ]


@router.get("/offices", response_model=list[Office], response_model_exclude_none=True)
@cache(expire=60 * 5)
async def get_offices() -> list[Office]:
    import uuid

    return [
        Office(
            id=uuid.uuid4(),
            address="AAA",
            coordinate=Coordinate(lat=55, lng=37),
            sale_point_name="AAA",
            schedule={
                Weekdays.FRI: OpenHours(opens_at=time(9, 0), closes_at=time(18, 0))
            },
        )
    ]
