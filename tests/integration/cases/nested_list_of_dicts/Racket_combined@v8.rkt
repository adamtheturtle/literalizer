#lang racket
(define my_data (list
    (list (hash "name" "Alice") (hash "name" "Bob"))
    (list (hash "name" "Charlie") (hash "name" "Dave"))
))
(set! my_data (list
    (list (hash "name" "Alice") (hash "name" "Bob"))
    (list (hash "name" "Charlie") (hash "name" "Dave"))
))
