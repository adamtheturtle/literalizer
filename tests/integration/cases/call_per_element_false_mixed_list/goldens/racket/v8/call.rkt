#lang racket
(define process (make-keyword-procedure (lambda _ (void))))
(process #:data (list 1 "x"))
