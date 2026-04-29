(defun process (&rest args) (declare (ignore args)) nil)
; Test cases
(process :value (list (cons "type" "create") (cons "pr_id" "pr_1")))  ; first case
(process :value (list (cons "type" "update") (cons "pr_id" "pr_2")))  ; second case
; third case
(process :value (list (cons "type" "delete") (cons "pr_id" "pr_3")))
