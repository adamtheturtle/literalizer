#lang racket
(define thing (make-keyword-procedure (lambda _ (void))))
(define thing.first_value (make-keyword-procedure (lambda _ (void))))
(thing.first_value #:value 1)
