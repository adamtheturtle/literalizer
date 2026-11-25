#lang racket
(define my_data (hash
    "first" (hash "items" (list 1 (hash "value" 2)))
    "second" (hash "items" (list 1 (hash "value" "s")))
))
