from fastapi import FastAPI
from router import test_router

app = FastAPI()

app.include_router(test_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8001)