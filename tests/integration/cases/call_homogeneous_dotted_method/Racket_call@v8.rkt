#lang racket
(define app (make-keyword-procedure (lambda _ (void))))
(define app.client (make-keyword-procedure (lambda _ (void))))
(define app.client.fetch (make-keyword-procedure (lambda _ (void))))
(app.client.fetch #:value "hello")
(app.client.fetch #:value "world")
