#lang racket
(define process (make-keyword-procedure (lambda _ (void))))
(process #:value (hash "a" 1 "b" "x"))
