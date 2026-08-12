#lang racket
(define my_data (hash
    "ordered" (hash
        ; ordered entry
        "name" "Alice"
        "scores" (hash
            ; score meaning
            1 "first"
            2 "second"  ; latest score
        )
    )
))
(set! my_data (hash
    "ordered" (hash
        ; ordered entry
        "name" "Alice"
        "scores" (hash
            ; score meaning
            1 "first"
            2 "second"  ; latest score
        )
    )
))
