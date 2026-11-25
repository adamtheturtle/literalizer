#lang racket
(define my_data (hash
    "quote\"backslash\\" 1
    "line\nbreak" 2
    "$(literal)${text}" 3
    "RStr prefix" 4
))
