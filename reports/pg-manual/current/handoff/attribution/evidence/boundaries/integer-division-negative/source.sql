SELECT x/4 AS value FROM (VALUES(-5),(-1),(0),(5),(NULL)) v(x) ORDER BY x NULLS LAST;
