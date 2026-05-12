#lang racket
(define my_data (hash
    "level1" (hash "level2" (hash "level3" (hash "level4" (hash "value" "deep" "items" (list "a" "b"))) "sibling" 42) "tags" (list (hash "name" "tag1" "meta" (hash "priority" 1 "labels" (list "x" "y")))))
))
