#lang racket
(define obj (make-keyword-procedure (lambda _ (void))))
(define obj.ZKV (make-keyword-procedure (lambda _ (void))))
(obj.ZKV #:value 1)
