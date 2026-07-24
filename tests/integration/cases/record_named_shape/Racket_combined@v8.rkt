#lang racket
(define my_data (list
    (hash "id" 100 "label" "first entry" "enabled" #f "related_ids" (list 102 103))
    (hash "id" 101 "label" "second entry" "enabled" #t "related_ids" (list 100))
))
(set! my_data (list
    (hash "id" 100 "label" "first entry" "enabled" #f "related_ids" (list 102 103))
    (hash "id" 101 "label" "second entry" "enabled" #t "related_ids" (list 100))
))
