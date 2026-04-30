(defparameter *my_data* (list
    (cons "a" (list (cons "b" (list (cons "c" (list (cons "$ref" "deep")))))))
))
(setf *my_data* (list
    (cons "a" (list (cons "b" (list (cons "c" (list (cons "$ref" "deep")))))))
))
