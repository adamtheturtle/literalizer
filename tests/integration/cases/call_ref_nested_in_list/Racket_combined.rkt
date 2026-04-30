#lang racket
(define my_data (list
    (list (list (hash "$ref" "my_var") 42 "static"))
    (list (list (hash "$ref" "my_other") 7 "label"))
))
(set! my_data (list
    (list (list (hash "$ref" "my_var") 42 "static"))
    (list (list (hash "$ref" "my_other") 7 "label"))
))
