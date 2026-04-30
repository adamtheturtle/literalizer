(defparameter *my_data* (list
    (list (list (cons "$ref" "repeated_var")) 1)
    (list (list (cons "$ref" "single_var")) 0)
    (list (list (cons "$ref" "repeated_var")) 8)
))
(setf *my_data* (list
    (list (list (cons "$ref" "repeated_var")) 1)
    (list (list (cons "$ref" "single_var")) 0)
    (list (list (cons "$ref" "repeated_var")) 8)
))
