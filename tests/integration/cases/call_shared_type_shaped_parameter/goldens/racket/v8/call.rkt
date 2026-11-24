#lang racket
(define process (make-keyword-procedure (lambda _ (void))))
(process #:i32 1)
