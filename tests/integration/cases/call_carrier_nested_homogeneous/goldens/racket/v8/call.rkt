#lang racket
(define app (make-keyword-procedure (lambda _ (void))))
(define app.client (make-keyword-procedure (lambda _ (void))))
(define app.client.go (make-keyword-procedure (lambda _ (void))))
(app.client.go #:first_value (list 1) #:second_value (list 2))
