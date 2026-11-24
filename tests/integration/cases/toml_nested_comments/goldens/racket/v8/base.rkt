#lang racket
(define my_data (hash
    ; About the first dotted key.
    ; About the second dotted key.
    "dotted" (hash "first" 1 "second" 2)
    "plain" 3  ; About the plain key.
    ; Before the first entry.
    ; Before the second entry.
    "entries" (list (hash "name" "one") (hash "name" "two"))
    ; Inside the table.
    "table" (hash "inner" 4)
))
