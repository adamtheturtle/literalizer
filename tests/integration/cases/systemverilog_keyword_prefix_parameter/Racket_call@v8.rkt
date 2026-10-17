#lang racket
(define make_widget (make-keyword-procedure (lambda _ (void))))
(make_widget #:first_value 1)
