SELECT CAST('{"a":null, "b":"qq"}' AS JSONB) ?& ARRAY('a', 'a', 'b', 'b', 'b');
