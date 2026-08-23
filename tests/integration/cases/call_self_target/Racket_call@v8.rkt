#lang racket
(define self (make-keyword-procedure (lambda _ (void))))
(self #:value "hello")
