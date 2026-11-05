#lang racket
(define consume_widget (make-keyword-procedure (lambda _ (void))))
(consume_widget #:arg_value (set
    1
    2
))
