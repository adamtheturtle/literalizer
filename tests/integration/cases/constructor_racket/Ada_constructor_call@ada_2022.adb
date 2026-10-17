#lang racket

(define (Playlist) 42)

p : A_Val := Playlist;
(unless (= p 42) (error "Expected constructor result"))
