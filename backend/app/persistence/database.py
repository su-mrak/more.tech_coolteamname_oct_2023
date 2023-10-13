from geoalchemy2.types import Geometry
from sqlalchemy import BigInteger, Boolean, Column, MetaData, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.ext.declarative import declarative_base

from shared.ulid import ulid_as_uuid

metadata_obj = MetaData(schema="public")

Base = declarative_base()
Base.metadata = metadata_obj


class GeoObject(Base):
    __tablename__ = "atm"

    id = Column(  # noqa: A003
        BigInteger,
        primary_key=True,
        comment="id for internal usage, i.e. joins, selects",
    )  # noqa: A003
    internal_id = Column(
        UUID(as_uuid=True),
        unique=True,
        default=ulid_as_uuid,
        nullable=False,
        comment="id for external usage, i.e. in API",
    )

    address = Column(Text)
    coordinate = Column(Geometry(geometry_type="POINT", srid=4326, spatial_index=True))


class ATM(GeoObject):
    all_day = Column(Boolean, nullable=False, default=False)
    services = Column(JSONB)


class Office(GeoObject):
    sale_point_name = Column(Text)
