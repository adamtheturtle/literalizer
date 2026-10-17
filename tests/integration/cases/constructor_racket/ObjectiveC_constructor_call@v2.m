#lang racket

(define (Playlist) 42)

id p = Playlist();
(unless (= p 42) (error "Expected constructor result"))
