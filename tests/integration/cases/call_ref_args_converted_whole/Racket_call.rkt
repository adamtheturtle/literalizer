#lang racket
(define process (make-keyword-procedure (lambda _ (void))))
(define my-var (list
    1
    2
    3
))
(process #:data my-var)
