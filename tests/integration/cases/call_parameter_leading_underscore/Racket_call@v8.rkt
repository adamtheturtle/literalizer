#lang racket
(define f (make-keyword-procedure (lambda _ (void))))
(f #:_x 1)
