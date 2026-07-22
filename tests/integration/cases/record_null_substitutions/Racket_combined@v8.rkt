#lang racket
(define my_data (list
    (hash "replacement" (void) "present" 1)
    (hash "replacement" 2 "present" 3)
))
(set! my_data (list
    (hash "replacement" (void) "present" 1)
    (hash "replacement" 2 "present" 3)
))
