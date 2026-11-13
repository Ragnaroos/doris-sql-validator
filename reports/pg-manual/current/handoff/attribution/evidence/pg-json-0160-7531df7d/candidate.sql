SELECT IF(JSON_EXTRACT_ISNULL('{"f2":{"f3":1},"f4":[0,1,2,null]}', '$.f4[3]'), NULL, JSON_EXTRACT_STRING('{"f2":{"f3":1},"f4":[0,1,2,null]}', '$.f4[3]')) IS NULL AS expect_true;
