#lang racket
(define process (make-keyword-procedure (lambda _ (void))))
(process #:a 1 #:b 2)
(process #:a 3 #:b 4)
