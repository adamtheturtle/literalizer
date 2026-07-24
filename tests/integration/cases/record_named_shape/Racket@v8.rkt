#lang racket
(define my_data (list
    (hash "id" 100 "label" "first item" "enabled" #f "related_ids" (list 102 103))
    (hash "id" 101 "label" "second item" "enabled" #t "related_ids" (list 100))
))
