#lang racket
(define foo (make-keyword-procedure (lambda _ (void))))
(define foo.Foo (make-keyword-procedure (lambda _ (void))))
(define foo.Foo.bar (make-keyword-procedure (lambda _ (void))))
(foo.Foo.bar #:x (list 1))
