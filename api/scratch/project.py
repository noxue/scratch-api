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


@router.get("")
async def project_list(page: int = 1, size: int = 10):
    session = Session()
    try:
        if page <= 0 or size <= 0:
            return {"status": 'error', "message": "页数或页码不对"}

        offset = (page - 1) * size

        total = session.query(Project).count()

        res = session.query(Project).offset(offset).limit(size).all()
        projects = list()
        for v in res:
            projects.append({"id": v.id, "title": v.title,
                            "create_time": v.create_time, "user_id": v.user_id})

        return {"status": 'ok', "data": {"projects": projects, "total": total}}
    except Exception as e:
        log.error(e)
        return {"status": 'error', "message": e}
    finally:
        session.close()


@router.get("/{id}/data")
async def get(id: int):
    session = Session()
    try:
        project: Project = session.query(
            Project).filter(Project.id == id).one()
        if project is None:
            return {"status": 'error', "message": "作品不存在"}
        return json.loads(project.data)
    except Exception as e:
        log.error(e)
        return {"status": 'error', "message": e}
    finally:
        session.close()


@router.get("/{id}")
async def get(id: int):
    session = Session()
    try:
        project: Project = session.query(
            Project).filter(Project.id == id).one()
        if project is None:
            return {"status": 'error', "message": "作品不存在"}
        del (project.data)
        return {"status": 'ok', "data": project}
    except Exception as e:
        log.error(e)
        return {"status": 'error', "message": e}
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
        if project is None:
            return {"status": 'error', 'message': '作品不存在'}

        if project.user_id != user['user_id']:
            return {"status": 'error', 'message': '不是你的作品，无权编辑'}

        project.title = title
        project.data = await req.body()
        session.commit()
        return {"status": "ok", "autosave-interval": "120"}
    except Exception as e:
        log.error(e)
        return {"status": 'error'}
    finally:
        session.close()
