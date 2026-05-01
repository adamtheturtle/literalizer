#lang racket
(define send (make-keyword-procedure (lambda _ (void))))
(send #:value (hash "a" 1 "b" "x"))
