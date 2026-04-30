#lang racket
(define process (make-keyword-procedure (lambda _ (void))))
(define my_var 42)
(define my_other 7)
(process #:data (list (hash "ref" "my_var") 42 "static"))
(process #:data (list (hash "ref" "my_other") 7 "label"))
