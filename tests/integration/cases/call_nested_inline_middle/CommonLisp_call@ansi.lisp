(defun f (&rest args) (declare (ignore args)) nil)
(f :ops (list (list "DEL" "b" "10") (list "ADD" "a" "x")))  ; note
; next call
(f :ops (list (list "ADD" "c" "y")))
