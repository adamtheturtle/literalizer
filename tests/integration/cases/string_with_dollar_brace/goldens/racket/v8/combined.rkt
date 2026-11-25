#lang racket
(define my_data (list
    "prefix ${HOME} suffix"
    "${interpolated}"
))
(set! my_data (list
    "prefix ${HOME} suffix"
    "${interpolated}"
))
