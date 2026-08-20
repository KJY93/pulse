from __future__ import annotations # import this as the | operator only works on python 3.10 and above
from app.schemas import SubscribeMessage
from pydantic import ValidationError
import logging

def parse_subscribe_message(raw_text: str) -> list[str] | None:
    try:
        sub_model = SubscribeMessage.model_validate_json(raw_text)
        return sub_model.symbols
    except ValidationError as e:
        logging.warning("an error has occured: %s", e)
        return None
