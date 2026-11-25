#lang racket
(define f (make-keyword-procedure (lambda _ (void))))
(f #:_ 1)
