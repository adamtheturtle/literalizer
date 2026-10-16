#lang racket
(define my_data (hash
    ; heading
    "a" "single ' // data"
    "b" "linecontinuation"
    "c" "\\"  ; actual comment
    "d" "  "  ; final comment
))
(set! my_data (hash
    ; heading
    "a" "single ' // data"
    "b" "linecontinuation"
    "c" "\\"  ; actual comment
    "d" "  "  ; final comment
))
