#lang racket
(define my_data (list
    (list "ADD" "alice" "hello")
    (list "DEL" "bob" "5")  ; removes "world"
))
(set! my_data (list
    (list "ADD" "alice" "hello")
    (list "DEL" "bob" "5")  ; removes "world"
))
