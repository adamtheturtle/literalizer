#lang racket
(define DoThing (make-keyword-procedure (lambda _ (void))))
(DoThing #:x 1)
(DoThing #:x 2)
