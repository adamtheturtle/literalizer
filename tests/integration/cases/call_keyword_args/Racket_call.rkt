#lang racket
(define throttler (make-keyword-procedure (lambda _ 0)))
(define throttler.check (make-keyword-procedure (lambda _ 0)))
(define emit (make-keyword-procedure (lambda _ (void))))
(emit (throttler.check #:user_id "user_1" #:ts 1000.0))
(emit (throttler.check #:user_id "user_2" #:ts 2000.5))
