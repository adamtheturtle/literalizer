(defun process (&rest args) (declare (ignore args)) nil)
(defparameter *my_var* 42)
(process :data (list (cons "key" (list (cons "ref" "my_var"))) (cons "count" 42)))
