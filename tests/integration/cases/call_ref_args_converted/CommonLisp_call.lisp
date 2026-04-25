(defun process (&rest args) (declare (ignore args)) nil)
(defparameter *my-var* (list
    1
    2
    3
))
(defparameter *my-other* (list
    4
    5
    6
))
(process :data *my-var* :count 42)
(process :data *my-other* :count 7)
