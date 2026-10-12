#lang racket
(define obj (make-keyword-procedure (lambda _ (void))))
(define obj.ZVal (make-keyword-procedure (lambda _ (void))))
(obj.ZVal #:value 1)
