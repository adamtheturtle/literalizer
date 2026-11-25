(define f (lambda args (if #f #f)))
(f (list (list "DEL" "b" "10") (list "ADD" "a" "x")))  ; note
; next call
(f (list (list "ADD" "c" "y")))
