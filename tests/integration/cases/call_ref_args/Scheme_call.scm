(define process (lambda args (if #f #f)))
(define my_var (list
    1
    2
    3
))
(define my_other (list
    4
    5
    6
))
(process my_var 42)
(process my_other 7)
