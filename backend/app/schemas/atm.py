import enum
import uuid

from pydantic import Field

from schemas.geo import GeoObject


class Features(str, enum.Enum):
    BLIND = "BLIND"
    NFC_FOR_BANK_CARDS = "NFC_FOR_BANK_CARDS"
    QR_READ = "QR_READ"
    SUPPORT_CHARGE_RUB = "SUPPORT_CHARGE_RUB"
    WHEELCHAIR = "WHEELCHAIR"

    WITHDRAWAL_EUR = "WITHDRAWAL_EUR"
    REPLENISHMENT_EUR = "REPLENISHMENT_EUR"
    WITHDRAWAL_RUB = "WITHDRAWAL_RUB"
    REPLENISHMENT_RUB = "REPLENISHMENT_RUB"
    WITHDRAWAL_USD = "WITHDRAWAL_USD"
    REPLENISHMENT_USD = "REPLENISHMENT_USD"

    ALL_DAY = "ALL_DAY"


class ATM(GeoObject):
    id_: uuid.UUID = Field(..., alias="id")
    features: set[Features]
