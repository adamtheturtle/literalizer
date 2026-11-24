#lang racket
(define f (make-keyword-procedure (lambda _ (void))))
; selected heading
(f #:a 1 #:b 2)  ; selected inline
