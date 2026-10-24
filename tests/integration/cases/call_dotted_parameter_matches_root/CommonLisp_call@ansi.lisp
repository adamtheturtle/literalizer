(defun outer (&rest args) (declare (ignore args)) nil)
(defun outer.inner (&rest args) (declare (ignore args)) nil)
(outer.inner :outer 1 :n 2)
