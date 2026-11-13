from pymysql.constants import FIELD_TYPE

from doris_sql_validator.execution.doris import _MYSQL_TYPE_NAMES, _doris_type_name


def test_mysql_alias_does_not_turn_tinyint_into_char() -> None:
    assert FIELD_TYPE.TINY == FIELD_TYPE.CHAR
    assert _MYSQL_TYPE_NAMES[FIELD_TYPE.TINY] == "TINYINT"


class _Field:
    def __init__(self, *, charsetnr: int, length: int) -> None:
        self.charsetnr = charsetnr
        self.length = length


def test_doris_blob_wire_type_uses_charset_to_distinguish_string() -> None:
    assert _doris_type_name(FIELD_TYPE.BLOB, _Field(charsetnr=33, length=255)) == "STRING"
    assert _doris_type_name(FIELD_TYPE.BLOB, _Field(charsetnr=63, length=255)) == "BINARY"


def test_doris_boolean_wire_alias_uses_length_one() -> None:
    assert _doris_type_name(FIELD_TYPE.TINY, _Field(charsetnr=33, length=1)) == "BOOLEAN"
    assert _doris_type_name(FIELD_TYPE.TINY, _Field(charsetnr=33, length=4)) == "TINYINT"

