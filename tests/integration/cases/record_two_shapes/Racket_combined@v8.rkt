#lang racket
(define my_data (hash
    "user" (hash "id" 1 "name" "Alice")
    "project" (hash "title" "report" "tags" (list "draft" "urgent"))
))
(set! my_data (hash
    "user" (hash "id" 1 "name" "Alice")
    "project" (hash "title" "report" "tags" (list "draft" "urgent"))
))
