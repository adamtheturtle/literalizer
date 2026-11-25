#lang racket
(define process (make-keyword-procedure (lambda _ (void))))
(process #:using 1)
