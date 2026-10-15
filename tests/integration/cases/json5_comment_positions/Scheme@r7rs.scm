(define my_data (list
    ;
    ; document heading
    ; before the first entry
    ; after the key
    ; before the value
    (cons "counts" (list
        ; before the first item
        1  ; inline block after the comma
        ; before the second item
        2
        ; trailing inside the array
    ))  ; after the nested collection
    (cons "more" (list
        3
        ;
        ; block heading
        ; block continuation
        4  ; final inline
    ))
    ; trailing inside the object
    ; after the root
    ; after the document
))
