#lang racket
(define process (make-keyword-procedure (lambda _ (void))))
(process #:value 1)  ; trail \ .
(process #:value 2)  ; second
