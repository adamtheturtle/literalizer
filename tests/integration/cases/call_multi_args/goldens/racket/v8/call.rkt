#lang racket
(define process (make-keyword-procedure (lambda _ (void))))
(process #:value 1 #:count 42)
(process #:value 2 #:count 100)
