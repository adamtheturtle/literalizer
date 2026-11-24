#lang racket
(define my_data (hash
    "my-key" "value1"
    "another-key" "value2"
    "normal_key" "value3"
))
(set! my_data (hash
    "my-key" "value1"
    "another-key" "value2"
    "normal_key" "value3"
))
