from __future__ import annotations # import this as the | operator only works on python 3.10 and above
import json
import logging

def parse_subscribe_message(raw_text: str) -> list[str] | None:
    try:
        subcription_payload = json.loads(raw_text)
        symbols = subcription_payload["symbols"]

        if isinstance(symbols, list):
            return symbols
        else:
            logging.warning("symbols received is not in a list")
    except KeyError:
        logging.warning("invalid payload, missing symbols field")
    except json.JSONDecodeError:
        logging.warning("invalid payload format (not in JSON)")
    except Exception as e:
        logging.warning("an error has occured: %s", e)
    return None