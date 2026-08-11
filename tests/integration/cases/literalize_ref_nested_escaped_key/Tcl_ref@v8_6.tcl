set foo [dict create \
    "_" "_" \
]
set my_data [dict create \
    "items" [list [dict create "other" 1] foo] \
    "mapping" [dict create "value" foo] \
]
