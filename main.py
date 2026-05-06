from fastapi import FastAPI, Request, status, Depends, exceptions, Form
from pydantic import EmailStr
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException
from routers import play
import auth
from schemas import UserCreate

from sqlalchemy import select
from sqlalchemy.orm import Session
import model
from database import get_db, Base, engine

from typing import Annotated

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(play.router)
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

# Simple in-memory user storage (replace with database for production)
users_db = {}


@app.get("/", response_class=HTMLResponse)
@app.get("/home", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(request, "index.html")


@app.get("/login", response_class=HTMLResponse)
def get_login(request: Request):
    return templates.TemplateResponse(request, "login.html")

@app.post("/login")
def login_form_submit(db: Annotated[Session, Depends(get_db)], email: str = Form(...)):
    result = db.execute(select(model.User).where(model.User.email == email))
    existing_user = result.scalars().first()
    if not existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email does not exist")
    
    auth.current_user_id = existing_user.id
    auth.isLoggedIn = True


    return RedirectResponse(url="/play/game", status_code=status.HTTP_303_SEE_OTHER)
    


@app.get("/register", response_class=HTMLResponse)
def get_register(request: Request):
    return templates.TemplateResponse(request, "register.html")


@app.post("/register", status_code=status.HTTP_201_CREATED)
async def user_form_submit(user: UserCreate, db: Annotated[Session, Depends(get_db)]):
    """Handle user registration with JSON payload"""
    result = db.execute(select(model.User).where(model.User.username == user.username))
    existing_user = result.scalars().first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists")

    result = db.execute(select(model.User).where(model.User.email == user.email))
    existing_user = result.scalars().first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists")

    new_user = model.User(
        username=user.username,
        email=user.email 
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return JSONResponse(
            status_code=200,
            content={
        "message": "User registered successfully",
        "user": {
            "username": user.username,
            "email": user.email,
        }
    },
        )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle validation errors and return JSON response"""
    errors = exc.errors()
    error_details = []

    for error in errors:
        field = error["loc"][-1]
        msg = error["msg"]
        error_details.append(f"{field}: {msg}")

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": " | ".join(error_details)}
    )

@app.exception_handler(HTTPException)
def general_http_exception_handler(request: Request, exception: HTTPException):
    message = (
        exception.detail 
        if exception.detail 
        else "An error occurred. Please check your request and try again later."
    )

    return JSONResponse(
            status_code=exception.status_code,
            content={"detail": message},
        )

    # return templates.TemplateResponse(
    #     request,
    #     "error.html",
    #     {
    #         "status_code": exception.status_code,
    #         "title": f"Error {exception.status_code}",
    #         "message": message,
    #     },
    #     status_code=exception.status_code,
    # )