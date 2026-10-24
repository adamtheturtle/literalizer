(use-modules (json))
(define my_data (list
    (cons "a" (vector (list (cons "item" (vector 1)))))
    (cons "b" (vector (list (cons "item" (vector 2 3)))))
))
