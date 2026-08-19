from app.subscribe_parser import parse_subscribe_message

def test_valid_json_payload():
    valid_payload = '{"symbols": ["BTCUSDT", "ETHUSDT"]}'
    result = parse_subscribe_message(valid_payload)
    assert result == ["BTCUSDT", "ETHUSDT"]

def test_malformed_json_payload():
    malformed_payload = '{"symbols": ["BTCUSDT", "ETHUSDT" }'
    result = parse_subscribe_message(malformed_payload)
    assert result is None # to use is / is not for singletons check

def test_missing_key_from_json_payload():
    missing_key_payload = '{}'
    result = parse_subscribe_message(missing_key_payload)
    assert result is None

def test_wrong_symbol_type():
    wrong_symbol_type = '{"symbols": "BTCUSDT"}'
    result = parse_subscribe_message(wrong_symbol_type)
    assert result is None

def test_empty_payload():
    empty_payload = '{"symbols": []}'
    result = parse_subscribe_message(empty_payload)
    assert result == []