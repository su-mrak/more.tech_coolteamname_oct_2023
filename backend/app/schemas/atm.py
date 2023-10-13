from schemas.base import CamelizedBaseModel
from schemas.geo import GeoObject


class ServiceConfiguration(CamelizedBaseModel):
    service_activity: bool
    service_capability: bool


class Services(CamelizedBaseModel):
    blind: ServiceConfiguration
    nfc_for_bank_cards: ServiceConfiguration
    qr_read: ServiceConfiguration
    supports_charge_rub: ServiceConfiguration
    supports_eur: ServiceConfiguration
    supports_rub: ServiceConfiguration
    supports_usd: ServiceConfiguration
    wheelchair: ServiceConfiguration


class ATM(GeoObject):
    all_day: bool
    services: Services
