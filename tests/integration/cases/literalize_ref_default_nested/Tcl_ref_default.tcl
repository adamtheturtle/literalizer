set my_var [dict create \
    "_" "_" \
]
set item_var [dict create \
    "_" "_" \
]
set my_data [dict create \
    "key" my_var \
    "items" [list item_var [dict create "fallback" "value"]] \
]
