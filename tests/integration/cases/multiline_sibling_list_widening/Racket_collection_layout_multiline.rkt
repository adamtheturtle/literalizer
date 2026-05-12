#lang racket
(define my_data (hash
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
