set my_data [dict create \
    "omap_value" [dict create \
        "first" 1 \
    ] \
    "sibling_lists" [dict create \
        "numbers" [list \
            1 \
            2 \
        ] \
        "strings" [list \
            "x" \
            "y" \
        ] \
    ] \
    "ref_marker_present" [list \
        "\$keep" \
        "z" \
    ] \
]
