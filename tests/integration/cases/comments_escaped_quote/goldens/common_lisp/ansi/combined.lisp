(defparameter *my_data* (list
    (cons "key" "value \" # not a comment")  ; real
))
(setf *my_data* (list
    (cons "key" "value \" # not a comment")  ; real
))
