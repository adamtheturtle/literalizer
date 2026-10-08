#lang racket
(define do_thing (make-keyword-procedure (lambda _ (void))))
(do_thing #:x_ 1)
(do_thing #:x_ 2)
