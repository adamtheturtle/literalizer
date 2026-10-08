#lang racket
(define my_data (hash
    "__proto__" (hash "x" 1)
    "n" (hash "__proto__" 3)
    "y" 2
))
