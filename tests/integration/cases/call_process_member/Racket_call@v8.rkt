#lang racket
(define app (make-keyword-procedure (lambda _ (void))))
(define app.process (make-keyword-procedure (lambda _ (void))))
(define app.process.fetch (make-keyword-procedure (lambda _ (void))))
(app.process.fetch #:data (hash "data" "hello"))
(app.process.fetch #:data (hash "data" 42))
(app.process.fetch #:data (hash "data" #t))
