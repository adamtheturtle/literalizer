#lang racket
(define f (make-keyword-procedure (lambda _ (void))))
; scalar heading
; second heading line
; scalar inline
; inline continuation
; scalar trailing
(f #:a 42)
