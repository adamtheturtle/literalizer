#lang racket

(define (Playlist) 42)

let p = Playlist::new();
(unless (= p 42) (error "Expected constructor result"))
