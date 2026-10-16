(define my_data (list
    ; heading
    (cons "a" "single ' // data")
    (cons "b" "linecontinuation")
    (cons "c" "\\")  ; actual comment
    (cons "d" "  ")  ; final comment
))
(set! my_data (list
    ; heading
    (cons "a" "single ' // data")
    (cons "b" "linecontinuation")
    (cons "c" "\\")  ; actual comment
    (cons "d" "  ")  ; final comment
))
