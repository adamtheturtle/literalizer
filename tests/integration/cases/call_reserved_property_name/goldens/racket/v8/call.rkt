#lang racket
(define foo (make-keyword-procedure (lambda _ (void))))
(define foo.class (make-keyword-procedure (lambda _ (void))))
(foo.class #:value 1)
