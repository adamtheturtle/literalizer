#lang racket
(define f (make-keyword-procedure (lambda _ (void))))
(f #:a (list (list 1 2) (list 3)))
