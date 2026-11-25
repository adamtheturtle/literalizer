#lang racket
(define my_data (hash
    "numbers" (list 1 2)
    "nested" (hash "inner" (list 3))
    "mixed" (list 4 "five")
))
