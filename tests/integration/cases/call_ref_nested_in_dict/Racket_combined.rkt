#lang racket
(define my_data (list
    (list (hash "key" (hash "$ref" "my_var") "count" 42))
))
(set! my_data (list
    (list (hash "key" (hash "$ref" "my_var") "count" 42))
))
