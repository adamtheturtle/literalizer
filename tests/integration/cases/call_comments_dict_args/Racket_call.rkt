#lang racket
(define process (make-keyword-procedure (lambda _ (void))))
; Test cases
(process #:value (hash "type" "create" "pr_id" "pr_1"))  ; first case
(process #:value (hash "type" "update" "pr_id" "pr_2"))  ; second case
; third case
(process #:value (hash "type" "delete" "pr_id" "pr_3"))
