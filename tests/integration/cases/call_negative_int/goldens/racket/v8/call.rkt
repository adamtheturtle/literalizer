#lang racket
(define process (make-keyword-procedure (lambda _ (void))))
(process #:value -1)
(process #:value -2)
(process #:value -3)
