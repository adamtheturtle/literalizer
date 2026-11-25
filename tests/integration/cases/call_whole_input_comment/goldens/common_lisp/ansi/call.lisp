(defun f (&rest args) (declare (ignore args)) nil)
(f :a (list 1))  ; note
