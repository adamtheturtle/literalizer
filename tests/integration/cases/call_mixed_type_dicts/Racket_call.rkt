#lang racket
(define mgr (make-keyword-procedure (lambda _ (void))))
(define mgr.Op (make-keyword-procedure (lambda _ (void))))
(mgr.Op #:operation (hash "type" "create" "pr_id" "pr_1" "draft" #t))
(mgr.Op #:operation (hash "type" "create" "pr_id" "pr_2"))
