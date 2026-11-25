(defun process (&rest args) (declare (ignore args)) nil)
(process :value "hello" :label "a")
(process :value 42 :label "b")
(process :value t :label "c")
