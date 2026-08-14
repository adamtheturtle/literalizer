set deep [list \
    [list \
        "one" \
        "two" \
    ] \
    [list \
        "three" \
        "four" \
    ] \
]
set my_data [dict create \
    "a" [dict create \
        "b" [dict create \
            "c" deep \
        ] \
    ] \
]
