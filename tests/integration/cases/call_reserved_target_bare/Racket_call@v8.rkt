#lang racket
(define class (make-keyword-procedure (lambda _ (void))))
(class #:a 42)
