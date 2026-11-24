#lang racket
(define f (make-keyword-procedure (lambda _ (void))))
(f #:using 1)
