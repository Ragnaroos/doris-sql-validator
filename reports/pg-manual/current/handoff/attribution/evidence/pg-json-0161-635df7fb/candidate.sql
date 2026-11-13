SELECT JSONB_EXTRACT(CAST('{"f2":{"f3":1},"f4":{"f5":99,"f6":"stringy"}}' AS JSON), ARRAY('f4', 'f6'));
