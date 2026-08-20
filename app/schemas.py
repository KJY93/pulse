from pydantic import BaseModel


class SubscribeMessage(BaseModel):
    symbols: list[str]