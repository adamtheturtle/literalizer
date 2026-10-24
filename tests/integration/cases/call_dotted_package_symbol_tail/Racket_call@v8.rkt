#lang racket
(define helper (make-keyword-procedure (lambda _ (void))))
(define helper.list (make-keyword-procedure (lambda _ (void))))
(helper.list #:a 1)
