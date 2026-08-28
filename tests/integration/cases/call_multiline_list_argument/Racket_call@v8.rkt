#lang racket
(define process (make-keyword-procedure (lambda _ (void))))
(process #:xs (list
    1
    2
))
(process #:xs (list
    3
))
