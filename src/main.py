from fastapi import FastAPI
from Gyms.routes import gym_router
from contextlib import asynccontextmanager
from database.dbmain import init_db
from auth.routes import auth_router
from MembershipDetails.routes import membership_router
from config import Settings

# settings=Settings()
version="v1"
@asynccontextmanager
async def life_span(app:FastAPI):
    print(f'server started')
    await init_db()
    yield
    print(f'server stopped')
   
app=FastAPI(title="The Gym App",description="A Rest api for Gym App service ",version=version, lifespan= life_span)
app.include_router(gym_router,prefix=f"/api/{version}/gyms",tags=['gyms'])
app.include_router(auth_router,prefix=f"/api/{version}/auth",tags=['auth'])
app.include_router(membership_router,prefix=f"/api/{version}/membership",tags=['membership'])