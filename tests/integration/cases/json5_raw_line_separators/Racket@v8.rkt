#lang racket
(define my_data (hash
    "double" "a b"
    "single" "c d"
    ; A comment, which both separators would end.
    "both" "e f g"
    "continued" "hi"
    "escaped backslash" "j\\ k"
))
