SELECT JSONB_EXISTS_ANY('{"a":null, "b":"qq"}', ARRAY('b', 'a'));
