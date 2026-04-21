#lang racket
(define app (make-keyword-procedure (lambda _ 0)))
(define app.client (make-keyword-procedure (lambda _ 0)))
(define app.client.fetch (make-keyword-procedure (lambda _ 0)))
(define emit (make-keyword-procedure (lambda _ (void))))
(emit (app.client.fetch #:payload "hello"))
(emit (app.client.fetch #:payload 42))
(emit (app.client.fetch #:payload #t))
