#lang racket
(define my_data (hash
    "items" (list (hash "id" 1) (hash "id" 2 "count" 10) (hash "id" 3 "count" 20))
))
(set! my_data (hash
    "items" (list (hash "id" 1) (hash "id" 2 "count" 10) (hash "id" 3 "count" 20))
))
