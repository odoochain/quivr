from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, Query, UploadFile
from logger import get_logger
from middlewares.auth import AuthBearer, get_current_user
from modules.ingestion.entity.ingestion import IngestionEntity
from modules.ingestion.extensions.summary import SummaryIngestion
from modules.ingestion.service.ingestion import Ingestion
from modules.user.entity.user_identity import UserIdentity

ingestion_router = APIRouter()
logger = get_logger(__name__)

ingestion_service = Ingestion()


@ingestion_router.get(
    "/ingestion", dependencies=[Depends(AuthBearer())], tags=["Ingestion"]
)
async def list_ingestion(
    current_user: UserIdentity = Depends(get_current_user),
) -> List[IngestionEntity]:
    """
    Retrieve and list all the knowledge in a brain.
    """

    ingestions = ingestion_service.get_all_ingestions()
    return ingestions


@ingestion_router.post(
    "/ingestion/{ingestion_id}/process",
    dependencies=[Depends(AuthBearer())],
    tags=["Ingestion"],
)
async def process_ingestion(
    uploadFile: UploadFile,
    ingestion_id: UUID = None,
    current_user: UserIdentity = Depends(get_current_user),
    brain_id: UUID = Query(..., description="The ID of the brain"),
):
    if ingestion_id is None:
        raise ValueError("Ingestion ID is required")

    ingestion = ingestion_service.get_ingestion_by_id(ingestion_id)

    if ingestion.name == "summary":
        summary = SummaryIngestion(uploadFile, current_user, brain_id)
        return await summary.process_ingestion()

    return {"status": "ok"}