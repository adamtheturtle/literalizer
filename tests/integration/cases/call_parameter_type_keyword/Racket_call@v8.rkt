#lang racket
(define f (make-keyword-procedure (lambda _ (void))))
(f #:i32 1)
