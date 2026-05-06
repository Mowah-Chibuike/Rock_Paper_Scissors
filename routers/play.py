from fastapi import APIRouter, Request, Depends, status
from fastapi.responses import JSONResponse, HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from schemas import ChoiceBase
import random
import auth

from sqlalchemy import select
from sqlalchemy.orm import Session
import model
from database import get_db

from typing import Annotated

router = APIRouter(prefix="/play", tags=["play"])
templates = Jinja2Templates(directory="templates")


@router.get("/", response_class=HTMLResponse)
def play(request: Request):
    return templates.TemplateResponse(request, "play.html")


@router.get("/game", response_class=HTMLResponse)
def game(request: Request):
    print(auth.isLoggedIn)
    if (auth.isLoggedIn):
        return templates.TemplateResponse(request, "game.html")
    return RedirectResponse(url="/login")


@router.post("/api/game/")
def play_game(player_choice: ChoiceBase, db: Annotated[Session, Depends(get_db)]):
    """Play a game round"""
    choices = ["rock", "paper", "scissors"]
    player_choice = player_choice.choice.lower()

    print(player_choice)

    # Validate player choice
    if player_choice not in choices:
        return {
            "error": "Invalid choice. Must be 'rock', 'paper', or 'scissors'."
        }

    # AI makes a random choice
    ai_choice = random.choice(choices)
    print(ai_choice)


    # Determine winner
    if player_choice == ai_choice:
        result = "tie"
    elif (
        (player_choice == "rock" and ai_choice == "scissors")
        or (player_choice == "paper" and ai_choice == "rock")
        or (player_choice == "scissors" and ai_choice == "paper")
    ):
        result = "win"
    else:
        result = "lose"

    new_log = model.History(
        user_id=auth.current_user_id,
        player_choice=player_choice,
        ai_choice=ai_choice,
        result=result 
    )
    db.add(new_log)
    db.commit()
    db.refresh(new_log) 

    return {
        "player_choice": player_choice,
        "ai_choice": ai_choice,
        "result": result,
    }

@router.get("/api/history", response_class=JSONResponse)
def get_history(request: Request, db: Annotated[Session, Depends(get_db)]):
    stats = {
        "win": 0,
        "lose": 0,
        "tie": 0
    }

    result = db.execute(select(model.User).where(model.User.id == auth.current_user_id))
    existing_user = result.scalars().first()

    for stat in existing_user.history:
        stats[stat.result] += 1

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=stats
    )