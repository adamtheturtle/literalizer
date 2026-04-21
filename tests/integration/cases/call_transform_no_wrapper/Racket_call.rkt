#lang racket
(define process (make-keyword-procedure (lambda _ 0)))
(process #:value "hello")
(process #:value 42)
(process #:value #t)
