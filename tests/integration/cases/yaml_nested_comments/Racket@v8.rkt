#lang racket
(define my_data (hash
    "a" (hash
        ; inner note
        "b" 1  ; inline b
    )
    "list" (list
        1  ; first
        2  ; second
    )
))
