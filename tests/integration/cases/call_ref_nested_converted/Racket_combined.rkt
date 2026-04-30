#lang racket
(define my_data (list
    (list (list (hash "$ref" "myVar") 42 "static"))
))
(set! my_data (list
    (list (list (hash "$ref" "myVar") 42 "static"))
))
