(define process (lambda args (if #f #f)))
(process 1 "hello")
(process "two" #f)
(process 3.5 '())
