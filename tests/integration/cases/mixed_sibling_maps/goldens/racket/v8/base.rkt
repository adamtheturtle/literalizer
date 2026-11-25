#lang racket
(define my_data (list
    (list (hash "a" 1) (hash "a" (void)) 42)
    (list (hash "a" 1) (hash "a" "s") 42)
    (list (hash "a" 1) (hash "a" (void)))
    (list (hash "a" 1) (hash "a" "s"))
))
