#lang racket
(define a (make-keyword-procedure (lambda _ (void))))
(define a.foo (make-keyword-procedure (lambda _ (void))))
(define a.foo.Foo (make-keyword-procedure (lambda _ (void))))
(define a.foo.Foo.bar (make-keyword-procedure (lambda _ (void))))
(a.foo.Foo.bar #:x (list 1))
