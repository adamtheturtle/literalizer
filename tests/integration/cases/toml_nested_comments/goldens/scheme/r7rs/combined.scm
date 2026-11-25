(define my_data (list
    ; About the first dotted key.
    ; About the second dotted key.
    (cons "dotted" (list (cons "first" 1) (cons "second" 2)))
    (cons "plain" 3)  ; About the plain key.
    ; Before the first entry.
    ; Before the second entry.
    (cons "entries" (list (list (cons "name" "one")) (list (cons "name" "two"))))
    ; Inside the table.
    (cons "table" (list (cons "inner" 4)))
))
(set! my_data (list
    ; About the first dotted key.
    ; About the second dotted key.
    (cons "dotted" (list (cons "first" 1) (cons "second" 2)))
    (cons "plain" 3)  ; About the plain key.
    ; Before the first entry.
    ; Before the second entry.
    (cons "entries" (list (list (cons "name" "one")) (list (cons "name" "two"))))
    ; Inside the table.
    (cons "table" (list (cons "inner" 4)))
))
