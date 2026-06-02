(define my_data (list
    (list (cons "id" 100) (cons "description" "first task") (cons "is_done" #f) (cons "blocks" (list 102 103)))
    (list (cons "id" 101) (cons "description" "second task") (cons "is_done" #t) (cons "blocks" (list 100)))
))
(set! my_data (list
    (list (cons "id" 100) (cons "description" "first task") (cons "is_done" #f) (cons "blocks" (list 102 103)))
    (list (cons "id" 101) (cons "description" "second task") (cons "is_done" #t) (cons "blocks" (list 100)))
))
