(define process (lambda args (if #f #f)))
; Test cases
(process (list "type" "create" "pr_id" "pr_1"))  ; first case
(process (list "type" "update" "pr_id" "pr_2"))  ; second case
; third case
(process (list "type" "delete" "pr_id" "pr_3"))
