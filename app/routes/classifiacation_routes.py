from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from app.pyd import UserInDB
from typing import Annotated
from typing import List
from app.services.classification_services import predicated_class
from app.auth import (

    get_current_user
)


class_router = APIRouter(tags=['classification'])

@class_router.post("/classification_file")
async def upload_file(mp3_file: UploadFile = File(...),
                      current_user: UserInDB = Depends(get_current_user)):
    if not mp3_file.filename.lower().endswith('.mp3'):
        raise HTTPException(status_code=400, detail="Only MP3 files are allowed")

    try:
        return await predicated_class(mp3_file)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")


@class_router.post("/classification/batch")
async def batch_classification(files: List[UploadFile] = File(...),
                               current_user: UserInDB = Depends(get_current_user)):
    results = []
    for file in files:
        try:
            predicted_class = await predicated_class(file)
            results.append({
                "filename": file.filename,
                "class": predicted_class["predicted_class"]
            })
        except Exception as e:
            results.append({
                "filename": file.filename,
                "error": str(e)
            })
    return {"results": results}