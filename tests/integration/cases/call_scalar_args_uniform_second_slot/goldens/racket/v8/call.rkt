#lang racket
(define process (make-keyword-procedure (lambda _ (void))))
(process #:value "hello" #:label "a")
(process #:value 42 #:label "b")
(process #:value #t #:label "c")
