#lang racket
(define my_data (list
    "C:\\path\\to\\file"
    "back\\\\slash"
    "hello \\\"world\\\""
    "path\\to \"# file"
))
(set! my_data (list
    "C:\\path\\to\\file"
    "back\\\\slash"
    "hello \\\"world\\\""
    "path\\to \"# file"
))
