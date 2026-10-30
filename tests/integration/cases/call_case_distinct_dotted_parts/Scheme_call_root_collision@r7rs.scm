(define foo (lambda args (if #f #f)))
(define foo.Foo (lambda args (if #f #f)))
(define foo.Foo.bar (lambda args (if #f #f)))
(foo.Foo.bar (list 1))
