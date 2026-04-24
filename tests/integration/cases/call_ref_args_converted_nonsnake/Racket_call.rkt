#lang racket
(define process (make-keyword-procedure (lambda _ (void))))
(define my-var (list
    1
    2
    3
))
(define my-other (list
    4
    5
    6
))
(process #:data my-var #:count 42)
(process #:data my-other #:count 7)
