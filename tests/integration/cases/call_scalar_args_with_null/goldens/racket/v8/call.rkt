#lang racket
(define process (make-keyword-procedure (lambda _ (void))))
(process #:value (void))
(process #:value "hello")
