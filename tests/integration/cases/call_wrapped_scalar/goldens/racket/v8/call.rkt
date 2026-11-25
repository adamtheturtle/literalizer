#lang racket
(define make_widget (make-keyword-procedure (lambda _ (void))))
(make_widget #:value 1)
