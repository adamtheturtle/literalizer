#lang racket
(define process (make-keyword-procedure (lambda _ 0)))
(define my_data (process #:value 1))
