#lang racket
(define my_data (hash
    "rows" (list (hash "replacement" (void) "present" 1) (hash "replacement" 2 "present" 3))
))
(set! my_data (hash
    "rows" (list (hash "replacement" (void) "present" 1) (hash "replacement" 2 "present" 3))
))
