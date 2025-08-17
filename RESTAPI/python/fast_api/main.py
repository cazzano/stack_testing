# main.py

from fastapi import FastAPI

app = FastAPI()

@app.get("/api/hello")
async def read_hello():
    return {"message": "hello hi"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7000)
