(defparameter *my_data* (list
    (cons "ordered" (list
        ; ordered entry
        (cons "name" "Alice")
        (cons "scores" (list
            ; score meaning
            (cons 1 "first")
            (cons 2 "second")  ; latest score
        ))
    ))
))
(setf *my_data* (list
    (cons "ordered" (list
        ; ordered entry
        (cons "name" "Alice")
        (cons "scores" (list
            ; score meaning
            (cons 1 "first")
            (cons 2 "second")  ; latest score
        ))
    ))
))
