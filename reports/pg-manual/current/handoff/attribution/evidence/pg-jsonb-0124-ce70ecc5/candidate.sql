SELECT IF(JSON_EXTRACT_ISNULL(CAST('[{"b": "c"}, {"b": "cc"}]' AS JSONB), '$[1]'), NULL, JSON_EXTRACT_STRING(CAST('[{"b": "c"}, {"b": "cc"}]' AS JSONB), '$[1]'));
