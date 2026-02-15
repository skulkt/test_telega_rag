from fastapi import APIRouter, HTTPException, Depends, UploadFile, File
from fastapi.responses import JSONResponse

from api.schemas.base import ApiResponseBase
from core.config import logger
from application.services.rag import get_rag_service, RagService

router = APIRouter(prefix="/rag")


@router.get("/documents_count", response_model=ApiResponseBase[int])
async def documents_count(rag_service: RagService = Depends(get_rag_service)):
    try:
        count = await rag_service.get_documents_count()

        return JSONResponse(
            status_code=200,
            content=ApiResponseBase(code=200, data=count).model_dump(),
        )
    except Exception as e:
        logger.exception(f"Error occurred: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.post("/parse_file", response_model=ApiResponseBase)
async def parse_file(
    file: UploadFile = File(None), rag_service: RagService = Depends(get_rag_service)
):
    try:
        await rag_service.parse_file(await file.read())

        return JSONResponse(
            status_code=200, content=ApiResponseBase(code=200).model_dump()
        )
    except Exception as e:
        logger.exception(f"Error occurred: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get("/clear_database", response_model=ApiResponseBase)
async def clear_database(rag_service: RagService = Depends(get_rag_service)):
    try:
        await rag_service.clear_database()

        return JSONResponse(
            status_code=200, content=ApiResponseBase(code=200).model_dump()
        )
    except Exception as e:
        logger.exception(f"Error occurred: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
