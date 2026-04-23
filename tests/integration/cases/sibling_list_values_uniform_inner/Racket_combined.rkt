#lang racket
(define my_data (hash
    "lint" (list 2 (list 1))
    "test" (list 5 (list 7))
))
(set! my_data (hash
    "lint" (list 2 (list 1))
    "test" (list 5 (list 7))
))
