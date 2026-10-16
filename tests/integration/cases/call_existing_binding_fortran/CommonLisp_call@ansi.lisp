(defun make_widget (&rest args) (declare (ignore args)) 0)
(defparameter *my_data* (make_widget :count 0))
(setf *my_data* (make_widget :count 1))
