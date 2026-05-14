#lang racket
(define my_data (hash
    "name" "Alice"
    "scores" (hash 1 "first" 2 "second")
))
(set! my_data (hash
    "name" "Alice"
    "scores" (hash 1 "first" 2 "second")
))
