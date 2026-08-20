from __future__ import annotations

from pydantic import ValidationError # import this as the | operator only works on python 3.10 and above
from app.schemas import SubscribeMessage

print("=== 1. Malformed JSON ===")
try:
    SubscribeMessage.model_validate_json('{not valid json}')
except ValidationError as e:
    print(e)

print("\n=== 2. Missing symbols key ===")
try:
    SubscribeMessage.model_validate_json('{}')
except ValidationError as e:
    print(e)

print("\n=== 3. Wrong type (string instead of list) ===")
try:
    SubscribeMessage.model_validate_json('{"symbols": "BTCUSDT"}')
except ValidationError as e:
    print(e)

print("\n=== 4. Empty list ===")
try:
    result = SubscribeMessage.model_validate_json('{"symbols": []}')
    print(f"SUCCESS: {result}")
except ValidationError as e:
    print(e)

