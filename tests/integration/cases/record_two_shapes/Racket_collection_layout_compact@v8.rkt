#lang racket
(define my_data (hash
    "metrics" (hash "count" 100 "rate" 50)
    "flags" (hash "retries" 3 "timeout" 30)
))
