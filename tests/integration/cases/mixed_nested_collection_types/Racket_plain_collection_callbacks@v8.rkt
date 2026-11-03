#lang racket
(define my_data (hash
    "lists" (list (list 1) (list "x") (list ))
    "maps" (list (hash "x" 1) (hash "x" "s"))
    "empties" (hash "a" (list 1) "b" (list ))
))
