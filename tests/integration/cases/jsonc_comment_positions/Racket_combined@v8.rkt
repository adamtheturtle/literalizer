#lang racket
(define my_data (hash
    ;
    ; document heading
    ; before the first entry
    ; after the key
    ; before the value
    "counts" (list
        ; before the first item
        1  ; inline block after the comma
        ; before the second item
        2
        ; trailing inside the array
    )  ; after the nested collection
    "more" (list
        3
        ;
        ; block heading
        ; block continuation
        4  ; final inline
    )
    ; trailing inside the object
    ; after the root
    ; after the document
))
(set! my_data (hash
    ;
    ; document heading
    ; before the first entry
    ; after the key
    ; before the value
    "counts" (list
        ; before the first item
        1  ; inline block after the comma
        ; before the second item
        2
        ; trailing inside the array
    )  ; after the nested collection
    "more" (list
        3
        ;
        ; block heading
        ; block continuation
        4  ; final inline
    )
    ; trailing inside the object
    ; after the root
    ; after the document
))
