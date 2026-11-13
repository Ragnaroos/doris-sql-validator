SELECT CAST(CAST(ARRAY(ARRAY('a', 'bc'), ARRAY('def', 'hijk')) AS ARRAY<STRING>) AS ARRAY<VARCHAR>) AS `{{a,bc},{def,hijk}}`;
