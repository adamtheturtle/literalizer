#lang racket
(define process (make-keyword-procedure (lambda _ (void))))
(define my-var 42)
(process #:data (list (hash "ref" "myVar") 42 "static"))
