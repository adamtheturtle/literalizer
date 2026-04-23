(defun mgr (&rest args) (declare (ignore args)) nil)
(defun mgr.Op (&rest args) (declare (ignore args)) nil)
(mgr.Op :operation (list (cons "type" "create") (cons "pr_id" "pr_1") (cons "draft" t)))
(mgr.Op :operation (list (cons "type" "create") (cons "pr_id" "pr_2")))
