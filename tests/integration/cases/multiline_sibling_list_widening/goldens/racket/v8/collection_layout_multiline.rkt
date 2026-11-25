#lang racket
(define my_data (hash
    "omap_value" (hash
        "first" 1
    )
    "sibling_lists" (hash
        "numbers" (list
            1
            2
        )
        "strings" (list
            "x"
            "y"
        )
    )
    "ref_marker_present" (list
        "$keep"
        "z"
    )
))
