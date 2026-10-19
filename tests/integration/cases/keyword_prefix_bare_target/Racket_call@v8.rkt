#lang racket
(define first_value (make-keyword-procedure (lambda _ (void))))
(first_value #:value 1)
