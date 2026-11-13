SELECT CAST('{"a":null, "b":"qq"}' AS JSONB) ?& ARRAY('b', 'a');
