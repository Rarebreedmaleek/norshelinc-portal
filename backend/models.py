from pydantic import BaseModel
from typing import List, Dict, Optional
from datetime import datetime

class DailyActivities(BaseModel):
    morning: str
    afternoon: str

class WeeklyActivities(BaseModel):
    monday: DailyActivities
    tuesday: DailyActivities
    wednesday: DailyActivities
    thursday: DailyActivities
    friday: DailyActivities

class WeeklyLunchMenu(BaseModel):
    monday: str
    tuesday: str
    wednesday: str
    thursday: str
    friday: str

class Client(BaseModel):
    id: str
    name: str
    image_url: str
    team: str
    activities: WeeklyActivities

class ParentDashboard(BaseModel):
    clients: List[Client]
    lunch_menu: WeeklyLunchMenu

# Mock data
MOCK_LUNCH_MENU = WeeklyLunchMenu(
    monday="Rice & Beans",
    tuesday="Pasta",
    wednesday="Chicken Wrap",
    thursday="Sandwich",
    friday="Pizza"
)

MOCK_CLIENTS = [
    Client(
        id="1",
        name="John Doe",
        image_url="/static/colin-rivers.jpg",
        team="Team 2",
        activities=WeeklyActivities(
            monday=DailyActivities(morning="Art Class", afternoon="Swimming"),
            tuesday=DailyActivities(morning="Music Class", afternoon="Group Games"),
            wednesday=DailyActivities(morning="Movies", afternoon="Bowling"),
            thursday=DailyActivities(morning="Cooking Class", afternoon="Dance"),
            friday=DailyActivities(morning="Sports", afternoon="Arts & Crafts")
        )
    )
]

# Parent-Client relationships
PARENT_CLIENTS = {
    "parent1@norshel.com": ["1"]  # Parent has access to John Doe
}

# Authentication models
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

class Parent(BaseModel):
    email: str
    full_name: str
    disabled: Optional[bool] = None 