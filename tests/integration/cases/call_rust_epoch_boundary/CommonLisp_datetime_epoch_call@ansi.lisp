(defun consume (&rest args) (declare (ignore args)) nil)
(consume :value -2147483649)
(consume :value 2147483648)
