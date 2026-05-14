#lang racket
(define my_data (hash
    "description" "# not a comment\n"
    "name" "foo"
))
(set! my_data (hash
    "description" "# not a comment\n"
    "name" "foo"
))
