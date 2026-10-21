#lang racket
(define check (make-keyword-procedure (lambda _ (void))))
(check #:timestamp "2024-01-15T10:30:00+00:00" #:date_value (date 0 0 0 1 6 2024 6 152 #f 0))
