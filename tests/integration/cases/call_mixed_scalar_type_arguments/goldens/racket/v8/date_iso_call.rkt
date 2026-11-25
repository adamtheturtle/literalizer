#lang racket
(define capture (make-keyword-procedure (lambda _ (void))))
(capture #:nan_value +nan.0 #:positive_infinity +inf.0 #:negative_infinity -inf.0 #:finite_value 1.25 #:date_value "2024-01-15" #:datetime_value "2024-01-15T12:34:56" #:text_value "[ordinary text]")
