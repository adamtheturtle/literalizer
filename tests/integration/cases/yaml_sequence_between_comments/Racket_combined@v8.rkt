#lang racket
(define my_data (list
    (hash "item" "existing")
    ; This comment describes the next item.
    (hash "item" "next")
))
(set! my_data (list
    (hash "item" "existing")
    ; This comment describes the next item.
    (hash "item" "next")
))
