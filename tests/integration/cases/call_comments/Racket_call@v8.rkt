#lang racket
(define process (make-keyword-procedure (lambda _ (void))))
; Test cases
(process #:value "hello")  ; single word
(process #:value "hello world")  ; two words
; trailing comment
