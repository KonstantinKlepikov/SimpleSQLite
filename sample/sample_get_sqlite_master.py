#!/usr/bin/env python
# encoding: utf-8

from __future__ import print_function

import json

from simplesqlite import SimpleSQLite


con = SimpleSQLite("sample.sqlite", "w")
data_matrix = [[1, 1.1, "aaa", 1, 1], [2, 2.2, "bbb", 2.2, 2.2], [3, 3.3, "ccc", 3, "ccc"]]
con.create_table_from_data_matrix(
    "sample_table", ["a", "b", "c", "d", "e"], data_matrix, index_attrs=["a"]
)

print(json.dumps(con.fetch_sqlite_master(), indent=4))
