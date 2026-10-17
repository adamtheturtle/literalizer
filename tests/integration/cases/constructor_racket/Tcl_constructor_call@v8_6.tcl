#lang racket

(define (Playlist) 42)

set p [Playlist]
(unless (= p 42) (error "Expected constructor result"))
