(define process (lambda args (if #f #f)))
(define my-var 42)
(process (list (list "ref" "myVar") 42 "static"))
