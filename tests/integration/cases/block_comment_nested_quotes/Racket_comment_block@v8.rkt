#lang racket
(define my_data (hash
    #| "{-" and '{-' stay readable |#
    #| balanced {- nested -} and trailing -} stay readable |#
    "x" 1
))
