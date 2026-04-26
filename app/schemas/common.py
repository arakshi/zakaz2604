from datetime import date, datetime

from pydantic import BaseModel, EmailStr


class RoleOut(BaseModel):
    id: int
    name: str

    model_config = {"from_attributes": True}


class UserOut(BaseModel):
    id: int
    full_name: str
    email: EmailStr
    is_active: bool
    created_at: datetime
    role: RoleOut

    model_config = {"from_attributes": True}


class LoginIn(BaseModel):
    email: EmailStr
    password: str


class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"


class ClientIn(BaseModel):
    company_name: str
    contact_person: str
    phone: str
    email: EmailStr
    segment: str
    source: str


class ClientOut(ClientIn):
    id: int
    created_at: datetime

    model_config = {"from_attributes": True}


class DealIn(BaseModel):
    title: str
    client_id: int
    manager_id: int
    amount: float
    probability: float
    planned_close_date: date
    status: str = "active"


class DealOut(DealIn):
    id: int
    stage_id: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class TaskIn(BaseModel):
    title: str
    description: str = ""
    assigned_to: int
    related_deal_id: int | None = None
    due_date: date
    status: str = "new"
    priority: str = "medium"


class TaskOut(TaskIn):
    id: int
    created_at: datetime

    model_config = {"from_attributes": True}


class NotificationOut(BaseModel):
    id: int
    user_id: int
    text: str
    type: str
    is_read: bool
    created_at: datetime

    model_config = {"from_attributes": True}
