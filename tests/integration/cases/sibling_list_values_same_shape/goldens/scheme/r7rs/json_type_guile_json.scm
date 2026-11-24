(use-modules (json))
(define my_data (list
    (cons "test" (vector 5 (vector "compile" "test")))
    (cons "package" (vector 7 (vector "link" "test")))
))
