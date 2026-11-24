#lang racket
(define api (make-keyword-procedure (lambda _ (void))))
(define api.worker (make-keyword-procedure (lambda _ (void))))
(define api.worker.process (make-keyword-procedure (lambda _ (void))))
(api.worker.process #:values (list 1 (hash)) #:count 42)
(api.worker.process #:values (list 2 (hash "x" "s")) #:count 43)
