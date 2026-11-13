SELECT CAST(JSON_CONTAINS('{"a":"b", "b":1, "c":null}', '{"a":"b", "c":null}') AS BOOLEAN);
