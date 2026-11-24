#lang racket
(define my_data (hash
    "a_b" 1
    "a-b" 2
    "averyveryverylongkeynamethatgoesonandonandon" 3
    "averyveryverylongkeynamethatgoesonandmore" 4
))
(set! my_data (hash
    "a_b" 1
    "a-b" 2
    "averyveryverylongkeynamethatgoesonandonandon" 3
    "averyveryverylongkeynamethatgoesonandmore" 4
))
