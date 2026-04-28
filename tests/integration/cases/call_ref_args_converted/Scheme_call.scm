(define process (lambda args (if #f #f)))
(define my-var (list
    1
    2
    3
))
(define my-other (list
    4
    5
    6
))
(process my-var 42)
(process my-other 7)
