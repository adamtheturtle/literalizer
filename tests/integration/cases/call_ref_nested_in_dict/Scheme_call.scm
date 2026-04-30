(define process (lambda args (if #f #f)))
(define my_var 42)
(process (list "key" (list "ref" "my_var") "count" 42))
