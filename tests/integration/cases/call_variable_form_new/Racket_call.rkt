#lang racket
(define make_widget (make-keyword-procedure (lambda _ 0)))
(define result (make_widget #:count 42))
