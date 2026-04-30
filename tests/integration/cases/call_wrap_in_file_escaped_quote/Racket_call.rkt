#lang racket
(define process (make-keyword-procedure (lambda _ (void))))
(process #:v "a\"b")
