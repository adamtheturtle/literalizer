(defun process (&rest args) (declare (ignore args)) nil)
(process :value (list (cons "value" 1)))
(process :value (list (cons "value" "hello")))
