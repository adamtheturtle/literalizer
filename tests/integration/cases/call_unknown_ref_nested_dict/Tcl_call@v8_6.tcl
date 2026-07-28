proc process {args} {}
set my_list [dict create \
    "unused" "value" \
]
process [list [list [dict create "inner" my_list]]]
