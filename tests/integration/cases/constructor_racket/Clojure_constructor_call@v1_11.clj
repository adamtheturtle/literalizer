#lang racket

(define (Playlist) 42)

(def p (Playlist))
(unless (= p 42) (error "Expected constructor result"))
