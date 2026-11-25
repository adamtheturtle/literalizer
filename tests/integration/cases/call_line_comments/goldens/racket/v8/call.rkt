#lang racket
(define process (make-keyword-procedure (lambda _ (void))))
(process #:value "Dune")  ; first edition
(process #:value "Solaris")
(process #:value "Neuromancer")  ; cyberpunk
