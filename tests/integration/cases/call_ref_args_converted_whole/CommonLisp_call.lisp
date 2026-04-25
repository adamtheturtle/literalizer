(defun process (&rest args) (declare (ignore args)) nil)
(defparameter *my-var* (list
    1
    2
    3
))
(process :data *my-var*)
