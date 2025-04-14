from fastapi import FastAPI
from app.api import routes_system
# from app.middleware import setup_middlewares
# from app.logging_conf import configure_logging

app = FastAPI()

# configure_logging(app)
# setup_middlewares(app)

# app.include_router(routes_user.router, prefix='/users')
# app.include_router(routes_auth.router, prefix='/auth')
app.include_router(routes_system.router, prefix='/system')
