#lang racket
(define f (make-keyword-procedure (lambda _ (void))))
(f #:a 2 #:b "hello")  ; trailing note
; next element
(f #:a 3 #:b "world")
