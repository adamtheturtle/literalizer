#lang racket
(define my_data (list
    (list (hash "$ref" "repeated_var") 1)
    (list (hash "$ref" "single_var") 0)
    (list (hash "$ref" "repeated_var") 8)
))
(set! my_data (list
    (list (hash "$ref" "repeated_var") 1)
    (list (hash "$ref" "single_var") 0)
    (list (hash "$ref" "repeated_var") 8)
))
