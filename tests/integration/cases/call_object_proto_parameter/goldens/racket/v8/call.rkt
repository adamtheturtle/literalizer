#lang racket
(define capture (make-keyword-procedure (lambda _ (void))))
(capture #:__proto__ 1)
