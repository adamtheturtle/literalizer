#lang racket

(define (Playlist) 42)

data Val
    = PList (Array Val)
p = Playlist
(unless (= p 42) (error "Expected constructor result"))
