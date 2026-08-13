set deep [list \
    [list \
        1 \
        2 \
    ] \
    [list \
        3 \
        4 \
    ] \
]
set my_data [dict create \
    "a" [dict create \
        "b" [dict create \
            "c" deep \
        ] \
    ] \
]
