#lang racket
(define process (make-keyword-procedure (lambda _ (void))))
(define my_var 42)
(process #:data (hash "key" (hash "ref" "my_var") "count" 42))
