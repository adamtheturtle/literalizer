#lang racket
(define my_data (list
    (hash "missing" (void) "present" 1)
    (hash "missing" 2 "present" 3)
))
(set! my_data (list
    (hash "missing" (void) "present" 1)
    (hash "missing" 2 "present" 3)
))
