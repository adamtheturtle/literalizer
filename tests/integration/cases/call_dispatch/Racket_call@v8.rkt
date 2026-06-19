#lang racket
(define store_item (make-keyword-procedure (lambda _ (void))))
(define read_item (make-keyword-procedure (lambda _ (void))))
(store_item #:key 1 #:value 10)
(read_item #:key 1)
