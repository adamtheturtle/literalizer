(defun process (&rest args) (declare (ignore args)) nil)
(defparameter *my-var* 42)
(process :data (list (list (cons "ref" "myVar")) 42 "static"))
