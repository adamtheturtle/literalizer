(use-modules (json))
(define my_data (list
    (cons "$key" "a\"b\tcé #{world} $ident")
    (cons "trailing multi-byte" "café")
))
