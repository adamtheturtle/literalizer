#lang racket
(define f (make-keyword-procedure (lambda _ (void))))
(f #:x_ 1)
