set foo [dict create \
    "_" "_" \
]
set my_data [dict create \
    "mapping" [dict create "value" foo] \
    "items" [list [dict create "other" 1] foo] \
]
