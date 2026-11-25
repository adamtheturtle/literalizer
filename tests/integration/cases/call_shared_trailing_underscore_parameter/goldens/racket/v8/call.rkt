#lang racket
(define process (make-keyword-procedure (lambda _ (void))))
(process #:value_ 1)
