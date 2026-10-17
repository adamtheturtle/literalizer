#lang racket

(define (Playlist) 42)

(define p (Playlist))
(unless (= p 42) (error "Expected constructor result"))
