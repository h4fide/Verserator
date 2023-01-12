# from directory called API import file
from API import app


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app)