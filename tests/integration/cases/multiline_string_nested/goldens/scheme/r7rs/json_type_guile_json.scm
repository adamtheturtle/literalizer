(use-modules (json))
(define my_data (list
    (cons "outer" (vector (vector "nested first line\n  indented\n\nnested last line\n")))
))
