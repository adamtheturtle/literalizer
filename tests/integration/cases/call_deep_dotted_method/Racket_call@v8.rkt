#lang racket
(define obj (make-keyword-procedure (lambda _ (void))))
(define obj.api (make-keyword-procedure (lambda _ (void))))
(define obj.api.client (make-keyword-procedure (lambda _ (void))))
(define obj.api.client.post (make-keyword-procedure (lambda _ (void))))
(obj.api.client.post #:data "hello")
(obj.api.client.post #:data 42)
(obj.api.client.post #:data #t)
