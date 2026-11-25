(defun obj (&rest args) (declare (ignore args)) nil)
(defun obj.BEGIN (&rest args) (declare (ignore args)) nil)
(obj.BEGIN :a 42)
