#lang racket
(define my_data (hash
    "value" (hash "$ref" "foo")
))
(set! my_data (hash
    "value" (hash "$ref" "foo")
))
