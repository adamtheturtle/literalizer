#lang racket
(define process (make-keyword-procedure (lambda _ (void))))
(process #:values (list 1 (hash)) #:count 42)
