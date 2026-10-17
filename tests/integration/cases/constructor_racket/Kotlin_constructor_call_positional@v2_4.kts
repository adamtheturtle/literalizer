#lang racket

(define (Playlist) 42)

val p = Playlist()
(unless (= p 42) (error "Expected constructor result"))
