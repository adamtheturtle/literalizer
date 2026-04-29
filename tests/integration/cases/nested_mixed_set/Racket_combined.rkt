#lang racket
(define my_data (hash
    "name" "Alice"
    "tags" (set #t 42 "apple")
))
(set! my_data (hash
    "name" "Alice"
    "tags" (set #t 42 "apple")
))
