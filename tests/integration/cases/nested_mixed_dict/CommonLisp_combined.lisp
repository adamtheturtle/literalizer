(defparameter *my_data* (list
    (cons "outer" (list (cons "a" 1) (cons "b" "x") (cons "c" nil)))
))
(setf *my_data* (list
    (cons "outer" (list (cons "a" 1) (cons "b" "x") (cons "c" nil)))
))
