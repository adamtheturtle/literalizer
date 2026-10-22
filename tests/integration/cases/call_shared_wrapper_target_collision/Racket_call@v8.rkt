#lang racket
(define check (make-keyword-procedure (lambda _ (void))))
(check #:value 42)
