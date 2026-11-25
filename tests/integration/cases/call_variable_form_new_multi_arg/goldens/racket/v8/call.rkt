#lang racket
(define record_entry (make-keyword-procedure (lambda _ 0)))
(define my_data (record_entry #:s "a" #:n 1 #:b #t))
