proc process {args} {}
set single_var [list \
    4 \
    5 \
    6 \
]
set repeated_var 1
process repeated_var 1
process single_var 0
process repeated_var 8
