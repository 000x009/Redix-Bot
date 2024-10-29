from pydantic import BaseModel, AnyUrl


class Admin(BaseModel):
    user_id: int


class AdminConfig(BaseModel):
    admins: list


class WebConfig(BaseModel):
    web_app_url: AnyUrl
