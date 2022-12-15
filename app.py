import os
from fastapi import FastAPI, File, UploadFile, Request, Response, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from models.models import User, Project, session
from api import user, scratch
from log import log

# item = User(**{'name':'noxue', 'password':'123456'})
# session.add(item)
# session.commit()

app = FastAPI()

# 允许跨域
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:8601","http://127.0.0.1:5173","http://s.noxue.com"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

app.include_router(prefix='/api', router=user.router)
app.include_router(prefix="/api/scratch", router=scratch.project.router)



basePath = "./static/"

@app.post('/assets/{name}')
async def create_asset(name: str, req: Request):

    try:
        # 保存文件
        with open(basePath + name, 'wb') as f:
            # 写入文件
            f.write(await req.body())
        return {"status": 'ok', "content-name": name}
    except Exception as e:
        log.error(e)
        return "xxxxxx"


@app.get('/assets/internalapi/asset/{name}/get')
async def get_asset(name: str):
    # 判断文件是否存在
    if not os.path.exists(basePath + name):
        return ""
    
    # 读取文件
    return FileResponse(basePath + name, media_type='application/octet-stream')

thumbnailBase = "./thumbnails/"


@app.put('/thumbnail/{id}')  # 封面图片上传
async def update_thumbnail(id: int, req: Request):
    with open(thumbnailBase + '{}.png'.format(id), 'wb') as f:
        # 写入文件
        f.write(await req.body())
    return {"status": 'ok', "content-name": '{}.png'.format(id)}


@app.get('/thumbnail/{id}')
async def get_thumbnail(id: int):
    if not os.path.exists(thumbnailBase + '{}.png'.format(id)):
        return ""
    return FileResponse(thumbnailBase + '{}.png'.format(id), media_type='image/png')

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
