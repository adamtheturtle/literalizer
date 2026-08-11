#lang racket
(define my_data (hash
    "name" "Alice"
    ; score collection
    "scores" (hash
        ; score meaning
        1 "first"
        2 "second"  ; latest score
    )
))
