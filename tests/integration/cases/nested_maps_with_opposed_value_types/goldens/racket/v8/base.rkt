#lang racket
(define my_data (list
    (hash "input" (hash "name" "alice" "city" "paris") "expected" (hash "count" 1 "total" 2))
    (hash "input" (hash "name" 10 "city" 20) "expected" (hash "count" "done" "total" "pending"))
))
