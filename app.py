import logging
from enum import unique
import hashlib
import json
from sys import prefix
from fastapi import FastAPI, File, UploadFile, Request, Response, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from models.models import User, Project, session
from api import user

# item = User(**{'name':'noxue', 'password':'123456'})
# session.add(item)
# session.commit()

app = FastAPI(prefix="/api")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8601"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(prefix="/users", router=user.router)

projectBase = './projects/'


@app.get("/{id}")
async def get(id: int, response: Response):
    # 读取projects目录下的json文件
    f = open("{}{}.json".format(projectBase, id), 'rb')
    return StreamingResponse(f, media_type='application/octet-stream')


id = 1


@app.post("/")
async def create(req: Request, title: str = Query()):
    global id
    print(title)
    with open("{}{}.json".format(projectBase, id), 'wb') as f:
        # 写入文件
        f.write(await req.body())
    id += 1
    return {"status": 'ok', "content-name": "{}".format(id-1)}


@app.put("/{id}")
async def update(id: int, req: Request, title: str = Query()):
    print(title)
    with open("{}{}.json".format(projectBase, id), 'wb') as f:
        # 写入文件
        f.write(await req.body())
    return {"status": "ok", "autosave-interval": "2"}

basePath = "./static/"


@app.post('/assets/{name}')
async def create_asset(name: str, req: Request):

    # 保存文件
    with open(basePath + name, 'wb') as f:
        # 写入文件
        f.write(await req.body())
    return {"status": 'ok', "content-name": name}


@app.get('/assets/internalapi/asset/{name}/get')
async def get_asset(name: str):
    # 读取文件
    f = open(basePath + name, 'rb')
    return StreamingResponse(f, media_type='application/octet-stream')

thumbnailBase = "./thumbnails/"

# 封面


@app.put('/thumbnail/{id}')
async def update_thumbnail(id: int, req: Request):
    with open(thumbnailBase + '{}.png'.format(id), 'wb') as f:
        # 写入文件
        f.write(await req.body())
    return {"status": 'ok', "content-name": '{}.png'.format(id)}


# backpack
backpackBase = "./backpack/"

packs = {}


@app.post('/backpack/{username}')
async def backpack_admin(username: str, req: Request):
    data = await req.json()
    if packs.get(username) == None:
        packs[username] = []

    packs[username].append(data)
    print(data)
    return data


@app.get('/backpack/{data:path}')
async def backpack_get(data: str):
    return data
