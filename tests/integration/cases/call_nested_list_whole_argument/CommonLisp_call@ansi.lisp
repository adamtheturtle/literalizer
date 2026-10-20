(defun f (&rest args) (declare (ignore args)) nil)
(f :a (list (list 1 2) (list 3)))
