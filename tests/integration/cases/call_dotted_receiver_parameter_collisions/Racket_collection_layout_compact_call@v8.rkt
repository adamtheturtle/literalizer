#lang racket
(define api (make-keyword-procedure (lambda _ (void))))
(define api.worker (make-keyword-procedure (lambda _ (void))))
(define api.worker.process (make-keyword-procedure (lambda _ (void))))
(api.worker.process #:self (hash) #:self_ (hash))
