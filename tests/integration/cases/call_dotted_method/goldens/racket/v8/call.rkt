#lang racket
(define app (make-keyword-procedure (lambda _ (void))))
(define app.client (make-keyword-procedure (lambda _ (void))))
(define app.client.fetch (make-keyword-procedure (lambda _ (void))))
(app.client.fetch #:payload "hello")
(app.client.fetch #:payload 42)
(app.client.fetch #:payload #t)
