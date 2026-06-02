(define my_data (list
    (cons "key\nwith\nnewlines" "value1")
    (cons "key\twith\ttabs" "value2")
    (cons "" "value3")
))
(set! my_data (list
    (cons "key\nwith\nnewlines" "value1")
    (cons "key\twith\ttabs" "value2")
    (cons "" "value3")
))
