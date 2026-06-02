(define process (lambda args (if #f #f)))
; Test cases
(process (list (cons "type" "create") (cons "pr_id" "pr_1")))  ; first case
(process (list (cons "type" "update") (cons "pr_id" "pr_2")))  ; second case
; third case
(process (list (cons "type" "delete") (cons "pr_id" "pr_3")))
