from fastapi import FastAPI
from database import Base, engine
from routers.enrollment import router

Base.metadata.create_all(bind=engine)
app = FastAPI(
    title="Course Registration API"
)
app.include_router(router)