#lang racket
(define process (make-keyword-procedure (lambda _ 0)))
(define tracer (make-keyword-procedure (lambda _ (void))))
(define tracer.emit (make-keyword-procedure (lambda _ (void))))
(tracer.emit (process #:value "hello"))
(tracer.emit (process #:value 42))
(tracer.emit (process #:value #t))
