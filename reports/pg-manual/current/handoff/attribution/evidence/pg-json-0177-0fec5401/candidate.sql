SELECT JSONB_EXTRACT(CAST('{"a": {"b":{"c": "foo"}}}' AS JSON), ARRAY('a', 'b'));
