proc consume_widget {args} {}
set item [list \
    1 \
    2 \
]
set my_data [list \
    1 \
    2 \
]
consume_widget my_data
set my_data item
consume_widget my_data
