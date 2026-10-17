#lang racket

(define (Playlist) 42)

final p = Playlist();
(unless (= p 42) (error "Expected constructor result"))
