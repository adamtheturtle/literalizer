(defun send (&rest args) (declare (ignore args)) nil)
(send :value (list (cons "a" 1) (cons "b" "x")))
