#lang racket
(define process (make-keyword-procedure (lambda _ (void))))
(process #:value 1 #:extra "hello")
(process #:value "two" #:extra #f)
(process #:value 3.5 #:extra (void))
