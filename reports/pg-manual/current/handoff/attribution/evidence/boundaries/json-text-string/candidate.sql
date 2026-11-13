SELECT IF(JSON_EXTRACT_ISNULL('{"x":"a\\nb"}','$.x'),NULL,JSON_EXTRACT_STRING('{"x":"a\\nb"}','$.x')) AS value;
