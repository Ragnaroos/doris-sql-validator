SELECT IF(JSON_EXTRACT_ISNULL('{"x":null}','$.x'),NULL,JSON_EXTRACT_STRING('{"x":null}','$.x')) AS value;
