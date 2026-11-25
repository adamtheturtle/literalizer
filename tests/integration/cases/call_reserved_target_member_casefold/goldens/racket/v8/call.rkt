#lang racket
(define obj (make-keyword-procedure (lambda _ (void))))
(define obj.BEGIN (make-keyword-procedure (lambda _ (void))))
(obj.BEGIN #:a 42)
