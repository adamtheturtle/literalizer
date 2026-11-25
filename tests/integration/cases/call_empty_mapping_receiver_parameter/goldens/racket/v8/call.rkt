#lang racket
(define api (make-keyword-procedure (lambda _ (void))))
(define api.process (make-keyword-procedure (lambda _ (void))))
(api.process #:self (hash))
