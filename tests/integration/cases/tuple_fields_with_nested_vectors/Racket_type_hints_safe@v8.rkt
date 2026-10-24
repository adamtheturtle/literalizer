#lang racket
(define my_data (hash
    "lint" (list 2 (list))
    "test" (list 5 (list "compile"))
    "package" (list 7 (list "link" "test"))
))
