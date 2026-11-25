#lang racket
(define my_data (hash
    "a" 9223372036854775807
    "b" 9223372036854775808
))
(set! my_data (hash
    "a" 9223372036854775807
    "b" 9223372036854775808
))
