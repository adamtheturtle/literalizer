(defun process (&rest args) (declare (ignore args)) nil)
; Test cases
(process :value "hello")  ; single word
(process :value "hello world")  ; two words
; trailing comment
