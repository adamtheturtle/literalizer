(define process (lambda args (if #f #f)))
(process "hello" "a")
(process 42 "b")
(process #t "c")
