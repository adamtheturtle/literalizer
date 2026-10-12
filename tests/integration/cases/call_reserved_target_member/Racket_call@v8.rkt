#lang racket
(define obj (make-keyword-procedure (lambda _ (void))))
(define obj.class (make-keyword-procedure (lambda _ (void))))
(obj.class #:a 42)
