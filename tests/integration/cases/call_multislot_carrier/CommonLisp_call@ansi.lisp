(defun process (&rest args) (declare (ignore args)) nil)
(process :value 1 :extra "hello")
(process :value "two" :extra nil)
(process :value 3.5d0 :extra nil)
