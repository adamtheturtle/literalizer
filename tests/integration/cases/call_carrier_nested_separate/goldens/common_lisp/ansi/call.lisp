(defun app (&rest args) (declare (ignore args)) nil)
(defun app.client (&rest args) (declare (ignore args)) nil)
(defun app.client.go (&rest args) (declare (ignore args)) nil)
(app.client.go :first_value (list 1) :second_value (list "text"))
