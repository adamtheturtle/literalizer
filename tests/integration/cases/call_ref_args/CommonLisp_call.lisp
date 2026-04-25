(defun process (&rest args) (declare (ignore args)) nil)
(defparameter *my_var* (list
    1
    2
    3
))
(defparameter *my_other* (list
    4
    5
    6
))
(process :data *my_var* :count 42)
(process :data *my_other* :count 7)
