proc consume_widget {args} {}
set shared [list \
    1 \
    2 \
]
set my_data [list \
    0 \
]
consume_widget my_data
set my_data shared
consume_widget my_data
