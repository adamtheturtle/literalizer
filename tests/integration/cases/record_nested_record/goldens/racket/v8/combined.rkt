#lang racket
(define my_data (hash
    "id" 1
    "owner" (hash "name" "Alice" "age" 30)
))
(set! my_data (hash
    "id" 1
    "owner" (hash "name" "Alice" "age" 30)
))
