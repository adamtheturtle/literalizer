#lang racket
(define my_data (hash
    "schema" (hash "$ref" "#/defs/Foo")
))
(set! my_data (hash
    "schema" (hash "$ref" "#/defs/Foo")
))
