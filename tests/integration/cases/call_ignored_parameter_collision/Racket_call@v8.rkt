#lang racket
(define f (make-keyword-procedure (lambda _ (void))))
(f #:x 1 #:_x 2)
