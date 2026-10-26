#lang racket
(define my_data (hash
    "below" (list (list (list (list (list (list (list (list 1))))))))
    "boundary" (list (list (list (list (list (list (list (list (list 2)))))))))
    "multiple" (list (list (list (list (list (list (list (list (list (list (list (list (list (list (list (list (list 3)))))))))))))))))
    "text" (list (list (list (list (list (list (list (list (list "value")))))))))
    "boolean" (list (list (list (list (list (list (list (list (list #t)))))))))
    "float" (list (list (list (list (list (list (list (list (list 1.5)))))))))
))
