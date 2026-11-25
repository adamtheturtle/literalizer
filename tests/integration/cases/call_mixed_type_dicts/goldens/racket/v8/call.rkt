#lang racket
(define app (make-keyword-procedure (lambda _ (void))))
(define app.mgr (make-keyword-procedure (lambda _ (void))))
(define app.mgr.run (make-keyword-procedure (lambda _ (void))))
(app.mgr.run #:operation (hash "type" "create" "pr_id" "pr_1" "draft" #t))
(app.mgr.run #:operation (hash "type" "create" "pr_id" "pr_2"))
