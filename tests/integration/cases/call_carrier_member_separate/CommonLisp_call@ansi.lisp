(defun app (&rest args) (declare (ignore args)) nil)
(defun app.go (&rest args) (declare (ignore args)) nil)
(app.go :first_value (list 1) :second_value (list "text"))
