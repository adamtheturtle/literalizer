#lang racket
(define my_data (list
    (list
        (hash "item" "existing")
        "kept"
        ; This comment trails the first pair.
    )
    (list (hash "item" "next") "also kept")
    ; This comment describes the last pair.
    (list (hash "item" "last") "kept too")
))
