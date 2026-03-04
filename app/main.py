from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message":"User Service is up and running!"}

if __name__ =="__main__":
    import uvicorn
    uvicorn.run("main:app", reload=True)