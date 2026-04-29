#lang racket
(define my_data (hash
    "key" "value \" # not a comment"  ; real
))
(set! my_data (hash
    "key" "value \" # not a comment"  ; real
))
