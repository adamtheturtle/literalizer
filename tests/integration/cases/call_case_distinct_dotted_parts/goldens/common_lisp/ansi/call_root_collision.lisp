(defun foo (&rest args) (declare (ignore args)) nil)
(defun foo.Foo (&rest args) (declare (ignore args)) nil)
(defun foo.Foo.bar (&rest args) (declare (ignore args)) nil)
(foo.Foo.bar :x (list 1))
