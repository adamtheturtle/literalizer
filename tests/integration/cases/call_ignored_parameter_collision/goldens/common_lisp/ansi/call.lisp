(defun f (&rest args) (declare (ignore args)) nil)
(f :x 1 :_x 2)
