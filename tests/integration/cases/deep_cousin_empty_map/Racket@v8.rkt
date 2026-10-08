#lang racket
(define my_data (list
    (hash "outer" (hash "inner" (hash "x" 1)))
    (hash "outer" (hash "inner" (hash)))
))
