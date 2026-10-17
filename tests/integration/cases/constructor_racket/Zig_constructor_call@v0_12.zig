#lang racket

(define (Playlist) 42)

const p = Playlist();
(unless (= p 42) (error "Expected constructor result"))
