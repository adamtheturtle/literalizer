#lang racket
(define consume (make-keyword-procedure (lambda _ (void))))
(consume #:value 1)
