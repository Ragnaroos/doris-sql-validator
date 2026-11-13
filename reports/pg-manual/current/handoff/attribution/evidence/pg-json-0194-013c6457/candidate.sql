SELECT JSONB_EXTRACT_SCALAR(CAST('{"a": {"b":{"c": "foo"}}}' AS JSON), ARRAY('a'));
