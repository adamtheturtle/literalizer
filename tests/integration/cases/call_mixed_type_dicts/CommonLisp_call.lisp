(defun m (&rest args) (declare (ignore args)) nil)
(defun m.Op (&rest args) (declare (ignore args)) nil)
(m.Op :operation (list (cons "type" "create") (cons "pr_id" "pr_1") (cons "draft" t)))
(m.Op :operation (list (cons "type" "create") (cons "pr_id" "pr_2")))
