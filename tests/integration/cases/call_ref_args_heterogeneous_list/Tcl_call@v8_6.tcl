proc process {args} {}
set my_ints [list \
    1 \
    2 \
    3 \
]
set my_strings [list \
    "a" \
    "b" \
]
set my_empty [list ]
process my_ints 42
process my_strings 7
process my_empty 99
