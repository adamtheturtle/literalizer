(defun f (&rest args) (declare (ignore args)) nil)
(f :ops (list (list "DEL" "b" "10") (list "ADD" "a" "x")))  ; note
