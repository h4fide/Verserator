from fastapi.responses import JSONResponse, FileResponse, HTMLResponse
from fastapi import FastAPI, Query, Response, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from random import randint

from API.qrandom import randomlyric, songs_names

tags_metadata = [
    {
        "name": "Verserator",
        "description": "Its Give You Random Quotes From Songs",
    },
    {
        "name": "L'morphine API",
        "description": "L'morphine API by Verserator",
    },
]

app = FastAPI(
    title="Verserator", 
    description="Its Give You Random Quotes From Songs", 
    version="1.0.1" ,
    openapi_tags=tags_metadata)

app.mount("/static", StaticFiles(directory="API/static"), name="static")

templates = Jinja2Templates(directory="API/templates")

@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse("API/static/img/favicon.ico")


@app.get("/", tags=["Verserator"], response_class=HTMLResponse)
async def root(request: Request): 
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/api/v1/lmorphine", tags=["L'morphine API"])
async def get_random_quote(lyric: str = Query(None, regex="random"), popularity: int = Query(None, ge=1, le=30), songs: str = Query(None, regex="all|random"), track: int = Query(None, ge=1, le=30)):

    try:
        if lyric == "random" and popularity == None and track == None:
            return randomlyric(artist="lmorphine", file="TOP30")

        elif lyric == "random" and popularity != None:
            print(popularity)
            return randomlyric(artist="lmorphine", file="TOP30", songs_amnt=popularity)

        elif lyric == "random" and popularity == None and track != None:
            return randomlyric(artist="lmorphine", file="TOP30", track_number=track)

        elif lyric == "random" and popularity != None and track != None:
            return randomlyric(artist="lmorphine", file="TOP30", track_number=track)

        elif lyric == None and popularity == None and track == None:
            if songs == "all":
                return songs_names(artist="lmorphine", file="TOP30")
            elif songs == "random":
                songsnames = songs_names(artist="lmorphine", file="TOP30")
                return songsnames[randint(0, len(songsnames)-1)]
            else:
                return {"message": "Please use the correct query parameters. See the documentation for more information."}

        else:
            return {"message": "Please use the correct query parameters. See the documentation for more information."}
    except Exception as e:
        print("Error occured in get_random_quote function", e)
        return {"message": "Please use the correct query parameters. See the documentation for more information."}



@app.exception_handler(404)
async def page_not_found(request, exc):

    return JSONResponse(
        status_code=404,
        content={"message": "The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again."},
    )

