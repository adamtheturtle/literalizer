#lang racket
(define my_data (list
    (hash "id" 100 "description" "first task" "is_done" #f "blocks" (list 102 103))
    (hash "id" 101 "description" "second task" "is_done" #t "blocks" (list 100))
))
