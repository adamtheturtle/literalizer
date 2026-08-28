# About the first dotted key.
# About the second dotted key.
# About the plain key.
# Inside the table.
# Before the first entry.
# Before the second entry.
set my_data [dict create \
    "dotted" [dict create "first" 1 "second" 2] \
    "plain" 3 \
    "table" [dict create "inner" 4] \
    "entries" [list [dict create "name" "one"] [dict create "name" "two"]] \
]
