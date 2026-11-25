#lang racket
(define my_data (hash
    ; before
    "answer" 42  ; inline
    "plain" "ok"
    ; trailing
))
(set! my_data (hash
    ; before
    "answer" 42  ; inline
    "plain" "ok"
    ; trailing
))
