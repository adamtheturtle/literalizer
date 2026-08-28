(defparameter *my_data* (list
    (cons "flow" (list
        1
        ; After the first element.
        2
    ))
    ; Between the key and its value.
    (cons "gap" 3)
    ; On the block scalar header.
    (cons "block" "Text.
")
    (cons "nested" (list
        1
        1
        ; On the nested alias.
    ))
    (cons "anchored" 4)
    (cons "alias" 4)
    ; On the alias.
))
