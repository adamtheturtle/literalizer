#lang racket
(define process (make-keyword-procedure (lambda _ (void))))
(define process.api (make-keyword-procedure (lambda _ (void))))
(define process.api.fetch (make-keyword-procedure (lambda _ (void))))
(process.api.fetch #:data (hash "data" "hello"))
(process.api.fetch #:data (hash "data" 42))
(process.api.fetch #:data (hash "data" #t))
