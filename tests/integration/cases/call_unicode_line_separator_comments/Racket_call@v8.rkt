#lang racket
(define process (make-keyword-procedure (lambda _ (void))))
(process #:value 1)  ; note<U+2028>still commented<U+2029>done
