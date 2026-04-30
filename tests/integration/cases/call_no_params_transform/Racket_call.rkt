#lang racket
(define process (make-keyword-procedure (lambda _ 0)))
(define emit (make-keyword-procedure (lambda _ (void))))
(emit (process))
(emit (process))
