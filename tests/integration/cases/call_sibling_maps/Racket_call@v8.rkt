#lang racket
(define process (make-keyword-procedure (lambda _ (void))))
(process #:value (hash "value" 1))
(process #:value (hash "value" "hello"))
