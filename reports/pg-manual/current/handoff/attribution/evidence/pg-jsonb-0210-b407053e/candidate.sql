SELECT JSONB_EXISTS_ALL('{"a":null, "b":"qq"}', ARRAY('b', 'a'));
