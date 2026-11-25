#lang racket
(define f (make-keyword-procedure (lambda _ (void))))
(f #:a (list 1))  ; note
