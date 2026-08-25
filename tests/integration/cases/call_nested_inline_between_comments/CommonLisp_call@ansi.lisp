(defun f (&rest args) (declare (ignore args)) nil)
(f :a 2 :b "hello")  ; trailing note
; next element
(f :a 3 :b "world")
