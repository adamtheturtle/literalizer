#lang racket

(define (Playlist) 42)

Val : [
    RList (List Val),
]
p = Playlist
(unless (= p 42) (error "Expected constructor result"))
