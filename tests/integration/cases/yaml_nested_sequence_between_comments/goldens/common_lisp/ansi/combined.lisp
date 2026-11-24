(defparameter *my_data* (list
    (list
        (list (cons "item" "existing"))
        "kept"
        ; This comment trails the first pair.
    )
    (list (list (cons "item" "next")) "also kept")
    ; This comment describes the last pair.
    (list (list (cons "item" "last")) "kept too")
))
(setf *my_data* (list
    (list
        (list (cons "item" "existing"))
        "kept"
        ; This comment trails the first pair.
    )
    (list (list (cons "item" "next")) "also kept")
    ; This comment describes the last pair.
    (list (list (cons "item" "last")) "kept too")
))
