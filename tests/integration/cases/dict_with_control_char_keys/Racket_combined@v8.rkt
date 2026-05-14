#lang racket
(define my_data (hash
    "key\nwith\nnewlines" "value1"
    "key\twith\ttabs" "value2"
    "" "value3"
))
(set! my_data (hash
    "key\nwith\nnewlines" "value1"
    "key\twith\ttabs" "value2"
    "" "value3"
))
