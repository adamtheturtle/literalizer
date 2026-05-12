#lang racket
(define process (make-keyword-procedure (lambda _ (void))))
(process #:value "hello")
(process #:value 42)
(process #:value #t)
