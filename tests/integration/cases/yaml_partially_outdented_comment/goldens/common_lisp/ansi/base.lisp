(defparameter *my_data* (list
    (cons "a" (list
        (cons "b" (list 1))
        ; Outdented from the sequence, so the inner mapping claims this.
        (cons "c" 2)
    ))
    ; Outdented from the inner mapping too, so the root claims this.
    (cons "d" 3)
))
