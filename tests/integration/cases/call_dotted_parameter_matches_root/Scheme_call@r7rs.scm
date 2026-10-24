(define outer (lambda args (if #f #f)))
(define outer.inner (lambda args (if #f #f)))
(outer.inner 1 2)
