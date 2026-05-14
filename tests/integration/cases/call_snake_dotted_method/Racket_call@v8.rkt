#lang racket
(define my_app (make-keyword-procedure (lambda _ (void))))
(define my_app.http_client (make-keyword-procedure (lambda _ (void))))
(define my_app.http_client.fetch (make-keyword-procedure (lambda _ (void))))
(my_app.http_client.fetch #:payload "hello")
(my_app.http_client.fetch #:payload 42)
(my_app.http_client.fetch #:payload #t)
