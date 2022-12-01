from email import message
import json
from fastapi import APIRouter, Depends, Request, Query
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from log import log
from models.models import User, Session, Project
from utils import generate_jwt_token, hash_password, check_password, verify_token


router = APIRouter(
    prefix="/projects",
    tags=["projects"],
    responses={404: {"description": "Not found"}},
)


@router.get("/{id}")
async def get(id: int):
    session = Session()
    try:
        project: Project = session.query(
            Project).filter(Project.id == id).one()
        if project is None:
            return ""
        return json.loads(project.data)
    except Exception as e:
        log.error(e)
        return ""
    finally:
        session.close()


@router.post("/")
async def create(req: Request, title: str = Query(), user=Depends(verify_token)):
    project = Project(title=title, data=await req.body(), user_id=user['user_id'])
    session = Session()
    try:
        session.add(project)
        session.commit()
        return {"status": 'ok', "content-name": "{}".format(project.id)}
    except Exception as e:
        log.error(e)
        return {"status": 'error'}
    finally:
        session.close()
        

@router.put("/{id}")
async def update(id: int, req: Request, title: str = Query(), user=Depends(verify_token)):
    session = Session()
    try:
        project: Project = session.query(
            Project).filter(Project.id == id).first()
        project.title = title
        project.data = await req.body()
        session.commit()
        return {"status": "ok", "autosave-interval": "120"}
    except Exception as e:
        log.error(e)
        return {"status": 'error'}
    finally:
        session.close()
