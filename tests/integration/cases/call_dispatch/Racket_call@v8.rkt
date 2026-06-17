#lang racket
(define put (make-keyword-procedure (lambda _ (void))))
(define get (make-keyword-procedure (lambda _ (void))))
(put #:key 1 #:value 10)
(get #:key 1)
