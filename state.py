from pydantic import BaseModel, Field
from typing import TypedDict, Literal, Union 


class RouterState(TypedDict):
    email_subject: str
    email_body: str
    sender: str
    category: str
    summary: str
    key_points: str
    human_review: bool
    review_reason: str 
    needs_reply: bool              # NEW
    draft_reply: str 


class RouteDecision(BaseModel):
    category: Literal["sport", "finance", "tech", "applications", "miscellaneous"]
    reasoning: str


class DepartmentExtraction(BaseModel):
    summary: str
    key_points: str
    human_review: Union[str, bool] = Field(description="Review flag status")
    review_reason: str 
    needs_reply: bool = False      
    draft_reply: str = "" 
                      
