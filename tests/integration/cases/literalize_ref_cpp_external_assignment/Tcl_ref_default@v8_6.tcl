proc consume_widget {args} {}
set ref_data [list \
    1 \
    2 \
]
set my_data [list \
    0 \
]
consume_widget my_data
set my_data ref_data
consume_widget my_data
