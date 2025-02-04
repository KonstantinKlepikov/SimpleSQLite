#!/usr/bin/env python
# encoding: utf-8

from __future__ import print_function

from simplesqlite import SimpleSQLite


table_name = "sample_table"
con = SimpleSQLite("sample.sqlite", "w")

# create table -----
data_matrix = [[1, 1.1, "aaa", 1, 1], [2, 2.2, "bbb", 2.2, 2.2], [3, 3.3, "ccc", 3, "ccc"]]
con.create_table_from_data_matrix(
    table_name, ["attr_a", "attr_b", "attr_c", "attr_d", "attr_e"], data_matrix
)

# display data type for each column in the table -----
print(con.schema_extractor.fetch_table_schema(table_name).dumps())

# display values in the table -----
print("records:")
result = con.select(select="*", table_name=table_name)
for record in result.fetchall():
    print(record)
