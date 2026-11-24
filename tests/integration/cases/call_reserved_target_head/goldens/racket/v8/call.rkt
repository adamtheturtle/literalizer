#lang racket
(define class (make-keyword-procedure (lambda _ (void))))
(define class.member (make-keyword-procedure (lambda _ (void))))
(class.member #:a 42)
