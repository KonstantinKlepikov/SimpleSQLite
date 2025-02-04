# encoding: utf-8

from __future__ import absolute_import, unicode_literals

import string

import pytest
from pathvalidate import (
    InvalidCharError,
    InvalidReservedNameError,
    NullNameError,
    ValidReservedNameError,
    unprintable_ascii_chars,
)
from simplesqlite._validator import validate_sqlite_attr_name, validate_sqlite_table_name


__SQLITE_VALID_RESERVED_KEYWORDS = [
    "ABORT",
    "ACTION",
    "AFTER",
    "ANALYZE",
    "ASC",
    "ATTACH",
    "BEFORE",
    "BEGIN",
    "BY",
    "CASCADE",
    "CAST",
    "COLUMN",
    "CONFLICT",
    "CROSS",
    "CURRENT_DATE",
    "CURRENT_TIME",
    "CURRENT_TIMESTAMP",
    "DATABASE",
    "DEFERRED",
    "DESC",
    "DETACH",
    "EACH",
    "END",
    "EXCLUSIVE",
    "EXPLAIN",
    "FAIL",
    "FOR",
    "FULL",
    "GLOB",
    "IGNORE",
    "IMMEDIATE",
    "INDEXED",
    "INITIALLY",
    "INNER",
    "INSTEAD",
    "KEY",
    "LEFT",
    "LIKE",
    "MATCH",
    "NATURAL",
    "NO",
    "OF",
    "OFFSET",
    "OUTER",
    "PLAN",
    "PRAGMA",
    "QUERY",
    "RAISE",
    "RECURSIVE",
    "REGEXP",
    "REINDEX",
    "RELEASE",
    "RENAME",
    "REPLACE",
    "RESTRICT",
    "RIGHT",
    "ROLLBACK",
    "ROW",
    "SAVEPOINT",
    "TEMP",
    "TEMPORARY",
    "TRIGGER",
    "VACUUM",
    "VIEW",
    "VIRTUAL",
    "WITH",
    "WITHOUT",
]
__SQLITE_INVALID_RESERVED_KEYWORDS = [
    "ADD",
    "ALL",
    "ALTER",
    "AND",
    "AS",
    "AUTOINCREMENT",
    "BETWEEN",
    "CASE",
    "CHECK",
    "COLLATE",
    "COMMIT",
    "CONSTRAINT",
    "CREATE",
    "DEFAULT",
    "DEFERRABLE",
    "DELETE",
    "DISTINCT",
    "DROP",
    "ELSE",
    "ESCAPE",
    "EXCEPT",
    "EXISTS",
    "FOREIGN",
    "FROM",
    "GROUP",
    "HAVING",
    "IN",
    "INDEX",
    "INSERT",
    "INTERSECT",
    "INTO",
    "IS",
    "ISNULL",
    "JOIN",
    "LIMIT",
    "NOT",
    "NOTNULL",
    "NULL",
    "ON",
    "OR",
    "ORDER",
    "PRIMARY",
    "REFERENCES",
    "SELECT",
    "SET",
    "TABLE",
    "THEN",
    "TO",
    "TRANSACTION",
    "UNION",
    "UNIQUE",
    "UPDATE",
    "USING",
    "VALUES",
    "WHEN",
    "WHERE",
]

VALID_RESERVED_KEYWORDS_TABLE_UPPER = __SQLITE_VALID_RESERVED_KEYWORDS
INVALID_RESERVED_KEYWORDS_TABLE_UPPER = __SQLITE_INVALID_RESERVED_KEYWORDS + ["IF"]
VALID_RESERVED_KEYWORDS_TABLE_LOWER = [
    keyword.lower() for keyword in VALID_RESERVED_KEYWORDS_TABLE_UPPER
]
INVALID_RESERVED_KEYWORDS_TABLE_LOWER = [
    keyword.lower() for keyword in INVALID_RESERVED_KEYWORDS_TABLE_UPPER
]

VALID_RESERVED_KEYWORDS_ATTR_UPPER = __SQLITE_VALID_RESERVED_KEYWORDS + ["IF"]
INVALID_RESERVED_KEYWORDS_ATTR_UPPER = __SQLITE_INVALID_RESERVED_KEYWORDS
VALID_RESERVED_KEYWORDS_ATTR_LOWER = [
    keyword.lower() for keyword in VALID_RESERVED_KEYWORDS_ATTR_UPPER
]
INVALID_RESERVED_KEYWORDS_ATTR_LOWER = [
    keyword.lower() for keyword in INVALID_RESERVED_KEYWORDS_ATTR_UPPER
]

UTF8_WORDS = [["あいうえお"], ["属性"]]


class Test_validate_sqlite_table_name(object):
    @pytest.mark.parametrize(
        ["value"],
        [
            ["{}a".format(keyword)]
            for keyword in (
                VALID_RESERVED_KEYWORDS_TABLE_UPPER
                + INVALID_RESERVED_KEYWORDS_TABLE_UPPER
                + VALID_RESERVED_KEYWORDS_ATTR_UPPER
                + INVALID_RESERVED_KEYWORDS_ATTR_UPPER
            )
        ],
    )
    def test_normal_ascii(self, value):
        validate_sqlite_table_name(value)

    @pytest.mark.parametrize(["value"], UTF8_WORDS)
    def test_normal_utf8(self, value):
        validate_sqlite_table_name(value)

    @pytest.mark.parametrize(
        ["value"], [[first_char + "hoge123"] for first_char in string.digits + "%#!-*"]
    )
    def test_normal_non_alphabet_first_char(self, value):
        validate_sqlite_table_name(value)

    @pytest.mark.parametrize(
        ["value"],
        [["a{}b".format(invalid_c)] for invalid_c in unprintable_ascii_chars]
        + [["テ{}！!スト".format(invalid_c)] for invalid_c in unprintable_ascii_chars],
    )
    def test_exception_invalid_win_char(self, value):
        with pytest.raises(InvalidCharError):
            validate_sqlite_table_name(value)

    @pytest.mark.parametrize(
        ["value", "expected"],
        [[None, NullNameError], ["", NullNameError], [1, TypeError], [True, TypeError]],
    )
    def test_exception_type(self, value, expected):
        with pytest.raises(expected):
            validate_sqlite_table_name(value)

    @pytest.mark.parametrize(
        ["value", "expected"],
        [
            [reserved_keyword, ValidReservedNameError]
            for reserved_keyword in VALID_RESERVED_KEYWORDS_TABLE_UPPER
            + VALID_RESERVED_KEYWORDS_TABLE_LOWER
        ],
    )
    def test_exception_reserved_valid(self, value, expected):
        with pytest.raises(expected):
            validate_sqlite_table_name(value)

    @pytest.mark.parametrize(
        ["value", "expected"],
        [
            [reserved_keyword, InvalidReservedNameError]
            for reserved_keyword in INVALID_RESERVED_KEYWORDS_TABLE_UPPER
            + INVALID_RESERVED_KEYWORDS_TABLE_LOWER
        ],
    )
    def test_exception_reserved_invalid_name(self, value, expected):
        with pytest.raises(expected):
            validate_sqlite_table_name(value)


class Test_validate_sqlite_attr_name(object):
    @pytest.mark.parametrize(
        ["value"],
        [
            ["{}a".format(keyword)]
            for keyword in (
                VALID_RESERVED_KEYWORDS_TABLE_UPPER
                + INVALID_RESERVED_KEYWORDS_TABLE_UPPER
                + VALID_RESERVED_KEYWORDS_ATTR_UPPER
                + INVALID_RESERVED_KEYWORDS_ATTR_UPPER
                + ["_"]
            )
        ],
    )
    def test_normal_ascii(self, value):
        validate_sqlite_attr_name(value)

    @pytest.mark.parametrize(["value"], UTF8_WORDS)
    def test_normal_utf8(self, value):
        validate_sqlite_attr_name(value)

    @pytest.mark.parametrize(
        ["value"], [[first_char + "hoge123"] for first_char in string.digits + "%#!-*"]
    )
    def test_normal_non_alphabet_first_char(self, value):
        validate_sqlite_attr_name(value)

    @pytest.mark.parametrize(
        ["value"],
        [["a{}b".format(invalid_c)] for invalid_c in unprintable_ascii_chars]
        + [["テ{}！!スト".format(invalid_c)] for invalid_c in unprintable_ascii_chars],
    )
    def test_exception_invalid_win_char(self, value):
        with pytest.raises(InvalidCharError):
            validate_sqlite_attr_name(value)

    @pytest.mark.parametrize(
        ["value", "expected"],
        [[None, NullNameError], ["", NullNameError], [1, TypeError], [True, TypeError]],
    )
    def test_exception_type(self, value, expected):
        with pytest.raises(expected):
            validate_sqlite_attr_name(value)

    @pytest.mark.parametrize(
        ["value", "expected"],
        [
            [reserved_keyword, ValidReservedNameError]
            for reserved_keyword in VALID_RESERVED_KEYWORDS_ATTR_UPPER
            + VALID_RESERVED_KEYWORDS_ATTR_LOWER
        ],
    )
    def test_exception_reserved_valid(self, value, expected):
        with pytest.raises(expected):
            validate_sqlite_attr_name(value)

    @pytest.mark.parametrize(
        ["value", "expected"],
        [
            [reserved_keyword, InvalidReservedNameError]
            for reserved_keyword in INVALID_RESERVED_KEYWORDS_ATTR_UPPER
            + INVALID_RESERVED_KEYWORDS_ATTR_LOWER
        ],
    )
    def test_exception_reserved_invalid_name(self, value, expected):
        with pytest.raises(expected):
            validate_sqlite_attr_name(value)
