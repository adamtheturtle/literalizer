#lang racket
(define my_data (hash
    "name" "Alice"
    "scores" (hash
        ; score meaning
        1 "first"
        2 "second"  ; latest score
    )
))
(set! my_data (hash
    "name" "Alice"
    "scores" (hash
        ; score meaning
        1 "first"
        2 "second"  ; latest score
    )
))
