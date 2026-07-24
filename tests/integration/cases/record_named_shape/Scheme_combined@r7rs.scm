(define my_data (list
    (list (cons "id" 100) (cons "label" "first item") (cons "enabled" #f) (cons "related_ids" (list 102 103)))
    (list (cons "id" 101) (cons "label" "second item") (cons "enabled" #t) (cons "related_ids" (list 100)))
))
(set! my_data (list
    (list (cons "id" 100) (cons "label" "first item") (cons "enabled" #f) (cons "related_ids" (list 102 103)))
    (list (cons "id" 101) (cons "label" "second item") (cons "enabled" #t) (cons "related_ids" (list 100)))
))
