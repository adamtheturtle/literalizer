#lang racket
(define a (make-keyword-procedure (lambda _ 0)))
(define a.foo (make-keyword-procedure (lambda _ 0)))
(define a.foo.Foo (make-keyword-procedure (lambda _ 0)))
(define a.foo.Foo.bar (make-keyword-procedure (lambda _ 0)))
(define my_data (a.foo.Foo.bar #:x (list 1)))
