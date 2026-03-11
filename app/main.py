from fastapi import FastAPI

from routers import auth, users
from db.database import init_db


app = FastAPI()
app.include_router(auth.router)
app.include_router(users.router)
@app.on_event("startup")
async def start_up():
    await init_db()

@app.get("/")
def root():
    return {"message":"User Service is up and running!"}

if __name__ =="__main__":
    import uvicorn
    uvicorn.run("main:app", reload=True)