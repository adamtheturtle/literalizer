#lang racket
(define op (make-keyword-procedure (lambda _ (void))))
(op #:value "hello")
