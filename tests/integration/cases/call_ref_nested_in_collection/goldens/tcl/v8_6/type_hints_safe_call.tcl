proc process {args} {}
set big_list [list \
    "x" \
]
process [dict create "k" big_list] 2
