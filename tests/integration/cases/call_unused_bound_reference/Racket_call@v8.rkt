#lang racket
(define f (make-keyword-procedure (lambda _ (void))))
(f #:value (list 1 2))
