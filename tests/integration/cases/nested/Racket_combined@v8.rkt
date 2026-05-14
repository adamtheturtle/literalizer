#lang racket
(define my_data (hash
    "users" (list (hash "name" "Bob" "tags" (list "admin" "user")) (hash "name" "Carol" "tags" (list "guest")))
))
(set! my_data (hash
    "users" (list (hash "name" "Bob" "tags" (list "admin" "user")) (hash "name" "Carol" "tags" (list "guest")))
))
