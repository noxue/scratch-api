python -m venv .venv
pip install fastapi
pip install uvicorn
pip install sqlalchemy
pip install bcrypt
pip install "python-jose[cryptography]"
uvicorn app:app --port=9999 --reload

### nginx 反向代理中配置
```
if ( $request_method = 'OPTIONS' ) {
    add_header Access-Control-Allow-Origin $http_origin;
    add_header Access-Control-Allow-Methods 'GET,POST,PUT,DELETE,OPTIONS';
    add_header Access-Control-Allow-Headers Authorization,Content-Type,Accept,Origin,User-Agent,DNT,Cache-Control,X-Mx-ReqToken,X-Data-Type,X-Requested-With;
    add_header Access-Control-Allow-Credentials true;
    return 200;
}
```