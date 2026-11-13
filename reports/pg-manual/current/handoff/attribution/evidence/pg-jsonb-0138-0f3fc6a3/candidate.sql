SELECT CAST(JSON_CONTAINS('{"a":"b", "b":1, "c":null}', '{"g":null}') AS BOOLEAN);
