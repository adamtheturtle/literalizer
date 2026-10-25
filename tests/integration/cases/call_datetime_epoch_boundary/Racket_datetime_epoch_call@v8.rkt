#lang racket
(define consume (make-keyword-procedure (lambda _ (void))))
(consume #:value -2147483649)
(consume #:value 2147483648)
