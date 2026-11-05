# About the first dotted key.
# About the second dotted key.
# About the plain key.
# Before the first entry.
# Before the second entry.
# Inside the table.
set my_data [dict create \
    "dotted" [dict create "first" 1 "second" 2] \
    "plain" 3 \
    "entries" [list [dict create "name" "one"] [dict create "name" "two"]] \
    "table" [dict create "inner" 4] \
]
