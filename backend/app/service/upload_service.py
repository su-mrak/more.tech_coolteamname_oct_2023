from dataclasses import dataclass

import ujson
from tqdm import tqdm

from repository.db_repository import DbRepository
from schemas.atm import ServiceConfiguration, Services
from shared.base import logger


@dataclass
class UploadService:
    db_repository: DbRepository

    def __post_init__(self) -> None:
        self.atms_json_filename = "./app/data/atms.json"
        self.offices_json_filename = "./app/data/offices.json"

    async def upload(self) -> None:
        with open(self.atms_json_filename) as f:
            atms: list[dict] = ujson.load(f)["atms"]
            logger.info("Fetched {} atms", len(atms))

        with open(self.offices_json_filename) as f:
            offices: list[dict] = ujson.load(f)
            logger.info("Fetched {} offices", len(offices))

        for atm in tqdm(atms):
            await self.db_repository.insert_atm(
                address=atm["address"],
                all_day=atm["allDay"],
                services=Services(
                    blind=ServiceConfiguration(
                        service_activity=atm["services"]["blind"]["serviceActivity"]
                        == "AVAILABLE",
                        service_capability=atm["services"]["blind"]["serviceCapability"]
                        == "SUPPORTED",
                    ),
                    nfc_for_bank_cards=ServiceConfiguration(
                        service_activity=atm["services"]["nfcForBankCards"][
                            "serviceActivity"
                        ]
                        == "AVAILABLE",
                        service_capability=atm["services"]["nfcForBankCards"][
                            "serviceCapability"
                        ]
                        == "SUPPORTED",
                    ),
                    supports_charge_rub=ServiceConfiguration(
                        service_activity=atm["services"]["supportsChargeRub"][
                            "serviceActivity"
                        ]
                        == "AVAILABLE",
                        service_capability=atm["services"]["supportsChargeRub"][
                            "serviceCapability"
                        ]
                        == "SUPPORTED",
                    ),
                    supports_eur=ServiceConfiguration(
                        service_activity=atm["services"]["supportsEur"][
                            "serviceActivity"
                        ]
                        == "AVAILABLE",
                        service_capability=atm["services"]["supportsEur"][
                            "serviceCapability"
                        ]
                        == "SUPPORTED",
                    ),
                    supports_rub=ServiceConfiguration(
                        service_activity=atm["services"]["supportsRub"][
                            "serviceActivity"
                        ]
                        == "AVAILABLE",
                        service_capability=atm["services"]["supportsRub"][
                            "serviceCapability"
                        ]
                        == "SUPPORTED",
                    ),
                    supports_usd=ServiceConfiguration(
                        service_activity=atm["services"]["supportsUsd"][
                            "serviceActivity"
                        ]
                        == "AVAILABLE",
                        service_capability=atm["services"]["supportsUsd"][
                            "serviceCapability"
                        ]
                        == "SUPPORTED",
                    ),
                    qr_read=ServiceConfiguration(
                        service_activity=atm["services"]["qrRead"]["serviceActivity"]
                        == "AVAILABLE",
                        service_capability=atm["services"]["qrRead"][
                            "serviceCapability"
                        ]
                        == "SUPPORTED",
                    ),
                    wheelchair=ServiceConfiguration(
                        service_activity=atm["services"]["wheelchair"][
                            "serviceActivity"
                        ]
                        == "AVAILABLE",
                        service_capability=atm["services"]["wheelchair"][
                            "serviceCapability"
                        ]
                        == "SUPPORTED",
                    ),
                ).jsonable_encoder(),
                lng=atm["longitude"],
                lat=atm["latitude"],
            )
