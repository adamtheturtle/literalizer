#lang racket
(define check_wrapper (make-keyword-procedure (lambda _ (void))))
(check_wrapper #:a 42)
