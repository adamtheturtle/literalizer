#lang racket
(define BEGIN (make-keyword-procedure (lambda _ (void))))
(BEGIN #:a 42)
