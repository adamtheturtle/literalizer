#lang racket
(define my_data (hash
    "name" "Alice"
    "age" 30
    "active" #t
    "score" (void)
    "joined" (date 0 0 0 15 1 2024 1 14 #f 0)
    "last_login" "2024-01-15T12:30:00+00:00"
    "avatar" "48656c6c6f"
))
(set! my_data (hash
    "name" "Alice"
    "age" 30
    "active" #t
    "score" (void)
    "joined" (date 0 0 0 15 1 2024 1 14 #f 0)
    "last_login" "2024-01-15T12:30:00+00:00"
    "avatar" "48656c6c6f"
))
