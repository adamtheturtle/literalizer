#lang racket
(define Before (make-keyword-procedure (lambda _ (void))))
(Before #:value 1)
