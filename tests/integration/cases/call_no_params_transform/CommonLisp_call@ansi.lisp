(defun process (&rest args) (declare (ignore args)) 0)
(defun emit (&rest args) (declare (ignore args)) nil)
(emit (process))
(emit (process))
