#lang racket
(define my_data (hash
    "flow" (list
        1
        ; After the first element.
        2
    )
    ; Between the key and its value.
    "gap" 3
    ; On the block scalar header.
    "block" "Text.\n"
    "anchored" 4
    "alias" 4
    ; On the alias.
))
(set! my_data (hash
    "flow" (list
        1
        ; After the first element.
        2
    )
    ; Between the key and its value.
    "gap" 3
    ; On the block scalar header.
    "block" "Text.\n"
    "anchored" 4
    "alias" 4
    ; On the alias.
))
