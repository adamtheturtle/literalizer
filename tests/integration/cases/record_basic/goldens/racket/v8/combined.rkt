#lang racket
(define my_data (hash
    "id" 1
    "label" "She said \"hello\", then waved"
    "enabled" #f
    "related_ids" (list 1 2 3)
))
(set! my_data (hash
    "id" 1
    "label" "She said \"hello\", then waved"
    "enabled" #f
    "related_ids" (list 1 2 3)
))
