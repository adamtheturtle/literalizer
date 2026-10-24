#lang racket
(define thing (make-keyword-procedure (lambda _ (void))))
(define thing.Before (make-keyword-procedure (lambda _ (void))))
(thing.Before #:value 1)
