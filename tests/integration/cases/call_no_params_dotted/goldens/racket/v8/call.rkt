#lang racket
(define throttler (make-keyword-procedure (lambda _ (void))))
(define throttler.check (make-keyword-procedure (lambda _ (void))))
(throttler.check)
(throttler.check)
