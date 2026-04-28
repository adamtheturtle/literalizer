#lang racket
(define process (make-keyword-procedure (lambda _ 0)))
(define log (make-keyword-procedure (lambda _ (void))))
(define log.emit (make-keyword-procedure (lambda _ (void))))
(log.emit (process #:value "hello"))
(log.emit (process #:value 42))
(log.emit (process #:value #t))
