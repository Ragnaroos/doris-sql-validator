SELECT IF(JSON_EXTRACT_ISNULL('{"x":1}','$.missing'),NULL,JSON_EXTRACT_STRING('{"x":1}','$.missing')) AS value;
