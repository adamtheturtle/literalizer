#lang racket
(define make_widget (make-keyword-procedure (lambda _ 0)))
(set! my_data (make_widget #:count 42))
