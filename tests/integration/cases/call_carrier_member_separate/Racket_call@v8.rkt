#lang racket
(define app (make-keyword-procedure (lambda _ (void))))
(define app.go (make-keyword-procedure (lambda _ (void))))
(app.go #:first_value (list 1) #:second_value (list "text"))
