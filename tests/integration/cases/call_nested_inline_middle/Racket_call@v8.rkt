#lang racket
(define f (make-keyword-procedure (lambda _ (void))))
(f #:ops (list (list "DEL" "b" "10") (list "ADD" "a" "x")))  ; note
; next call
(f #:ops (list (list "ADD" "c" "y")))
