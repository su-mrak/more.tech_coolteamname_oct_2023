from dataclasses import dataclass

from repository.db_repository import DbRepository
from service.heath_service import HeathService
from service.upload_service import UploadService
from service.view_service import ViewService
from supplier.ort_supplier import ORTSupplier


@dataclass
class Container:
    heath_service: HeathService
    upload_service: UploadService
    view_service: ViewService


def init_combat_container() -> Container:
    db_repository = DbRepository()
    heath_service = HeathService(db_repository=db_repository)
    upload_service = UploadService(db_repository=db_repository)
    ort_supplier = ORTSupplier()
    view_service = ViewService(db_repository=db_repository, ort_supplier=ort_supplier)

    return Container(
        heath_service=heath_service,
        upload_service=upload_service,
        view_service=view_service,
    )
