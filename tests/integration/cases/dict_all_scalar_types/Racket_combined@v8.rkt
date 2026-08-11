#lang racket
(define my_data (hash
    "s" "string"
    "i" 1
    "f" 1.5
    "b" #t
    "n" (void)
    "d" (date 0 0 0 15 1 2024 1 14 #f 0)
    "dt" "2024-01-15T12:00:00"
    "by" "48656c6c6f"
))
(set! my_data (hash
    "s" "string"
    "i" 1
    "f" 1.5
    "b" #t
    "n" (void)
    "d" (date 0 0 0 15 1 2024 1 14 #f 0)
    "dt" "2024-01-15T12:00:00"
    "by" "48656c6c6f"
))
