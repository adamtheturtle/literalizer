#lang racket

(define (Playlist) 42)

let mut p = Playlist::new();
(unless (= p 42) (error "Expected constructor result"))
