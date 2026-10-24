#lang racket
(define outer (make-keyword-procedure (lambda _ (void))))
(define outer.inner (make-keyword-procedure (lambda _ (void))))
(outer.inner #:outer 1 #:n 2)
