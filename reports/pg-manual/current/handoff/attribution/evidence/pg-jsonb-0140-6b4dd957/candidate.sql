SELECT CAST(JSON_CONTAINS('{"a":"b", "b":1, "c":null}', '{"a":"b"}') AS BOOLEAN);
