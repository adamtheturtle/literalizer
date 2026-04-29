#lang racket
(define my_data (hash
    "a" (hash "x" 1)
    "b" 2
))
(set! my_data (hash
    "a" (hash "x" 1)
    "b" 2
))
