#lang racket
(define m (make-keyword-procedure (lambda _ (void))))
(define m.Op (make-keyword-procedure (lambda _ (void))))
(m.Op #:operation (hash "type" "create" "pr_id" "pr_1" "draft" #t))
(m.Op #:operation (hash "type" "create" "pr_id" "pr_2"))
