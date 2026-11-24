#lang racket
(define my_data (hash
    "ancient_date" (date 0 0 0 1 3 1500 4 59 #f 0)
    "modern_date" (date 0 0 0 15 1 2024 1 14 #f 0)
    "before_date" (date 0 0 0 4 10 1582 1 276 #f 0)
    "gap_date" (date 0 0 0 10 10 1582 0 282 #f 0)
    "transition_date" (date 0 0 0 15 10 1582 5 287 #f 0)
    "after_date" (date 0 0 0 16 10 1582 6 288 #f 0)
    "before_naive" "1582-10-04T12:30:00.000001"
    "gap_naive" "1582-10-10T12:30:00.500000"
    "transition_positive" "1582-10-15T00:30:00+18:00"
    "transition_negative" "1582-10-15T23:30:00-18:00"
    "after_positive" "1582-10-16T00:30:00+18:00"
))
