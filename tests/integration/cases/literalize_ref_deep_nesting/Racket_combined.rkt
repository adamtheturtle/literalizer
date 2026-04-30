#lang racket
(define my_data (hash
    "a" (hash "b" (hash "c" (hash "$ref" "deep")))
))
(set! my_data (hash
    "a" (hash "b" (hash "c" (hash "$ref" "deep")))
))
