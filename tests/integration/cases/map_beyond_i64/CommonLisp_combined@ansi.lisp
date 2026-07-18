(defparameter *my_data* (list
    (cons "a" 9223372036854775807)
    (cons "b" 9223372036854775808)
))
(setf *my_data* (list
    (cons "a" 9223372036854775807)
    (cons "b" 9223372036854775808)
))
