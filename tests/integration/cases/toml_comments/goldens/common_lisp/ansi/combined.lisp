(defparameter *my_data* (list
    ; before
    (cons "answer" 42)  ; inline
    (cons "plain" "ok")
    ; trailing
))
(setf *my_data* (list
    ; before
    (cons "answer" 42)  ; inline
    (cons "plain" "ok")
    ; trailing
))
