#lang racket
(define my_data (list
    (hash "id" 1 "empty_map" (hash) "int_map" (hash 1 "a") "full_set" (set "x" "y") "empty_set" (set))
    (hash "id" 2 "empty_map" (hash) "int_map" (hash 1 "b") "full_set" (set "x") "empty_set" (set))
))
(set! my_data (list
    (hash "id" 1 "empty_map" (hash) "int_map" (hash 1 "a") "full_set" (set "x" "y") "empty_set" (set))
    (hash "id" 2 "empty_map" (hash) "int_map" (hash 1 "b") "full_set" (set "x") "empty_set" (set))
))
