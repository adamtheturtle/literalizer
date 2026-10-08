(defun foo (&rest args) (declare (ignore args)) nil)
(defun foo.class (&rest args) (declare (ignore args)) nil)
(foo.class :value 1)
