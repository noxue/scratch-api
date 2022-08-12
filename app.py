from fastapi import FastAPI, File, UploadFile, Request, Response, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from models.models import User, Project, session
from api import user, scratch

# item = User(**{'name':'noxue', 'password':'123456'})
# session.add(item)
# session.commit()

app = FastAPI()

app.include_router(prefix='/api', router=user.router)
app.include_router(prefix="/api/scratch", router=scratch.project.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8601"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
